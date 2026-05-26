#!/usr/bin/env bash
set -euo pipefail

# --- select metrics.jsonl (mtime preferred, lexicographic fallback) ---
LATEST_METRICS="$(
python - <<'PY'
import os, glob, json
paths = glob.glob("ChangeOntCode/outputs/**/metrics.jsonl", recursive=True)
paths = sorted(paths, key=lambda p: os.path.getmtime(p))
def has_co_debug(p):
    try:
        with open(p, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except Exception:
                    continue
                if obj.get("metric") == "co_debug":
                    return True
    except Exception:
        return False
    return False

co_paths = [p for p in paths if has_co_debug(p)]
if co_paths:
    print(co_paths[-1])
else:
    print(paths[-1] if paths else "")
PY
)"
if [ -z "$LATEST_METRICS" ]; then
  if command -v rg >/dev/null 2>&1; then
    LATEST_METRICS="$(rg --files -g 'metrics.jsonl' ChangeOntCode/outputs | sort | tail -n 1)"
  else
    LATEST_METRICS=""
  fi
fi
if [ -n "$LATEST_METRICS" ]; then
  if ! jq -e 'select(.metric=="co_debug")' "$LATEST_METRICS" >/dev/null 2>&1; then
    echo "WARNING: No co_debug found in latest metrics.jsonl; QA may not reflect CO run."
  fi
fi
echo "LATEST_METRICS=$LATEST_METRICS"
test -n "$LATEST_METRICS"

# --- use only the last run segment (from last header) to avoid multi-run duplication ---
RUN_METRICS="$LATEST_METRICS"
TMP_METRICS="$(
LATEST_METRICS="$LATEST_METRICS" python - <<'PY'
import json, tempfile, os
src = os.environ.get("LATEST_METRICS", "")
if not src:
    print("")
    raise SystemExit(0)
try:
    with open(src, "r", encoding="utf-8") as f:
        lines = f.readlines()
except Exception:
    print("")
    raise SystemExit(0)
last_header = None
for i, line in enumerate(lines):
    try:
        obj = json.loads(line)
    except Exception:
        continue
    if obj.get("record_type") == "header":
        last_header = i
if last_header is None:
    print("")
    raise SystemExit(0)
tmp = tempfile.NamedTemporaryFile(prefix="qa_metrics_", suffix=".jsonl", delete=False)
with open(tmp.name, "w", encoding="utf-8") as f:
    f.writelines(lines[last_header:])
print(tmp.name)
PY
)"
if [ -n "$TMP_METRICS" ]; then
  RUN_METRICS="$TMP_METRICS"
  trap 'rm -f "$TMP_METRICS"' EXIT
fi

FAILS=()

fail() {
  local name="$1" msg="$2" excerpt_cmd="$3"
  echo "FAIL: $name"
  echo "  $msg"
  echo "  Excerpt (first 5):"
  eval "$excerpt_cmd" | head -n 5 || true
  FAILS+=("$name")
}

pass() { echo "PASS: $1"; }

# 1) JSONL header present
if jq -e 'select(.record_type=="header" and .runner!=null and .agent!=null)' "$RUN_METRICS" >/dev/null; then
  pass "header_present"
else
  fail "header_present" "Missing header record with record_type/runner/agent" \
    "jq -c 'select(.record_type==\"header\")' \"$RUN_METRICS\""
fi

# 2) header update exactly once per t
BAD_T="$(jq -r 'select(.header_update_count!=null) | .t' "$RUN_METRICS" | sort -n | uniq -c | awk '$1!=1{print $2}' | head -n 1)"
if [ -z "$BAD_T" ]; then
  pass "header_update_once"
else
  fail "header_update_once" "t with count != 1 detected" \
    "jq -c 'select(.header_update_count!=null and .t==$BAD_T)' \"$RUN_METRICS\""
fi

# 3) header update source is run_update only
BAD_SRC="$(jq -r 'select(.header_update_source!=null) | .header_update_source' "$RUN_METRICS" | sort | uniq -c | awk '$2!="run_update"{print $2; exit}')"
if [ -z "$BAD_SRC" ]; then
  pass "header_update_source"
else
  fail "header_update_source" "Non-run_update source detected: $BAD_SRC" \
    "jq -c 'select(.header_update_source!=null and .header_update_source!=\"run_update\")' \"$RUN_METRICS\""
fi

# 4) scalar signals present
if jq -e 'select(.signals!=null and
  .signals["EC_Identity.same"]!=null and
  .signals["EC_Identity.last_d"]!=null and
  .signals["EB_GHVC.pressure"]!=null and
  .signals["EB_GHVC.mdl_gain"]!=null and
  .signals["EB_GHVC.birth_suggest"]!=null)' "$RUN_METRICS" >/dev/null; then
  pass "signals_present"
else
  fail "signals_present" "signals missing required keys" \
    "jq -c 'select(.signals!=null)' \"$RUN_METRICS\""
fi

# 5) identity_ok varies; last_d > 0 exists
HAS_ZERO="$(jq -r 'select(.signals!=null) | .signals["EC_Identity.same"]' "$RUN_METRICS" | awk '$1==0{print; exit}')"
HAS_ONE="$(jq -r 'select(.signals!=null) | .signals["EC_Identity.same"]' "$RUN_METRICS" | awk '$1==1{print; exit}')"
HAS_LASTD="$(jq -r 'first(select(.signals!=null and (.signals["EC_Identity.last_d"]|tonumber)>0) | .t) // empty' "$RUN_METRICS")"
if [ -n "$HAS_ZERO" ] && [ -n "$HAS_ONE" ] && [ -n "$HAS_LASTD" ]; then
  pass "identity_variation"
else
  fail "identity_variation" "identity_ok not varying or last_d never > 0" \
    "jq -c 'select(.signals!=null) | {t:.t,same:.signals[\"EC_Identity.same\"],last_d:.signals[\"EC_Identity.last_d\"]}' \"$RUN_METRICS\""
fi

# 6) GHVC birth suggests + count changes
HAS_BIRTH="$(jq -r 'first(select(.signals!=null and .signals["EB_GHVC.birth_suggest"]==1) | .t) // empty' "$RUN_METRICS")"
BIRTH_CHG="$(jq -r 'select(.birth_count!=null) | .birth_count' "$RUN_METRICS" | sort -n | uniq -c | wc -l | awk '$1>1{print}')"
if [ -n "$HAS_BIRTH" ] && [ -n "$BIRTH_CHG" ]; then
  pass "ghvc_birth"
else
  fail "ghvc_birth" "No birth_suggest==1 or birth_count not changing" \
    "jq -c 'select(.signals!=null or .birth_count!=null) | {t:.t,birth_suggest:.signals[\"EB_GHVC.birth_suggest\"],birth_count:.birth_count}' \"$RUN_METRICS\""
fi

# 7) mask semantics (allowlist or blocklist)
BAD_MASK="$(jq -r '
  select(.metric=="co_debug")
  | select(.translator_mask!=null and (.translator_mask|type=="array") and .action!=null)
  | (.mask_mode // "blocklist") as $mode
  | if $mode=="allowlist" then
      ((.translator_mask|index(.action))==null)
    elif $mode=="blocklist" then
      ((.translator_mask|index(.action))!=null)
    else false end
  | select(.) | .t' "$RUN_METRICS" | head -n 1)"
if [ -z "$BAD_MASK" ]; then
  pass "mask_semantics"
else
  fail "mask_semantics" "Mask contract violated at t=$BAD_MASK" \
    "jq -c 'select(.translator_mask!=null and .t==$BAD_MASK) | {t:.t,mode:.mask_mode,action:.action,mask:.translator_mask}' \"$RUN_METRICS\""
fi

# 8) co_debug once per t
BAD_T2="$(jq -r 'select(.metric=="co_debug") | .t' "$RUN_METRICS" | sort -n | uniq -c | awk '$1!=1{print $2}' | head -n 1)"
if [ -z "$BAD_T2" ]; then
  pass "co_debug_once"
else
  fail "co_debug_once" "co_debug count != 1 at t=$BAD_T2" \
    "jq -c 'select(.metric==\"co_debug\" and .t==$BAD_T2)' \"$RUN_METRICS\""
fi

echo
if [ "${#FAILS[@]}" -eq 0 ]; then
  echo "PASS: all checks"
  exit 0
else
  echo "FAIL: ${#FAILS[@]} check(s) failed -> ${FAILS[*]}"
  exit 1
fi
