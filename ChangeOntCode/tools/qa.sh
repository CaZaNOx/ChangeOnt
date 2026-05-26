#!/usr/bin/env bash
set -euo pipefail

LATEST_METRICS="$((python - <<'PY'
import os, glob, json
paths = sorted(glob.glob('ChangeOntCode/outputs/**/metrics.jsonl', recursive=True), key=lambda p: os.path.getmtime(p))
def has_co_debug(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    obj = json.loads(line)
                except Exception:
                    continue
                if obj.get('metric') == 'co_debug':
                    return True
    except Exception:
        return False
    return False
co = [p for p in paths if has_co_debug(p)]
print(co[-1] if co else (paths[-1] if paths else ''))
PY
) )"
LATEST_METRICS="${LATEST_METRICS#(}"
LATEST_METRICS="${LATEST_METRICS%)}"
if [ -z "$LATEST_METRICS" ]; then
  if command -v rg >/dev/null 2>&1; then
    LATEST_METRICS="$(rg --files -g 'metrics.jsonl' ChangeOntCode/outputs | sort | tail -n 1)"
  else
    LATEST_METRICS="$(find ChangeOntCode/outputs -name metrics.jsonl 2>/dev/null | sort | tail -n 1)"
  fi
fi

echo "LATEST_METRICS=$LATEST_METRICS"
test -n "$LATEST_METRICS"

RUN_METRICS="$LATEST_METRICS"
TMP_METRICS="$(LATEST_METRICS="$LATEST_METRICS" python - <<'PY'
import json, tempfile, os
src = os.environ.get('LATEST_METRICS', '')
if not src:
    print(''); raise SystemExit(0)
with open(src, 'r', encoding='utf-8') as f:
    lines = f.readlines()
last_header = None
for i, line in enumerate(lines):
    try:
        obj = json.loads(line)
    except Exception:
        continue
    if obj.get('record_type') == 'header':
        last_header = i
if last_header is None:
    print(''); raise SystemExit(0)
tmp = tempfile.NamedTemporaryFile(prefix='qa_metrics_', suffix='.jsonl', delete=False)
with open(tmp.name, 'w', encoding='utf-8') as f:
    f.writelines(lines[last_header:])
print(tmp.name)
PY
)"
if [ -n "$TMP_METRICS" ]; then
  RUN_METRICS="$TMP_METRICS"
  trap 'rm -f "$TMP_METRICS"' EXIT
fi

FAILS=()
fail(){ echo "FAIL: $1"; echo "  $2"; FAILS+=("$1"); }
pass(){ echo "PASS: $1"; }

pycheck() {
  RUN_METRICS="$RUN_METRICS" CHECK_NAME="$1" python - <<'PY'
import json, os, sys
path = os.environ['RUN_METRICS']
check = os.environ['CHECK_NAME']
rows = []
with open(path, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except Exception:
            pass
ok = False
if check == 'header_present':
    ok = any(r.get('record_type') == 'header' and r.get('runner') is not None and r.get('agent') is not None for r in rows)
elif check == 'signals_present':
    req = {'EC_Identity.same','EC_Identity.last_d','EB_GHVC.pressure','EB_GHVC.mdl_gain','EB_GHVC.birth_suggest'}
    ok = any(req.issubset(set((r.get('signals') or {}).keys())) for r in rows)
sys.exit(0 if ok else 1)
PY
}

if pycheck header_present; then pass header_present; else fail header_present "Missing header record with runner/agent"; fi

BAD_T="$(jq -r 'select(.header_update_count!=null) | .t' "$RUN_METRICS" | sort -n | uniq -c | awk '$1!=1{print $2}' | head -n 1)"
if [ -z "$BAD_T" ]; then pass header_update_once; else fail header_update_once "t with count != 1 detected"; fi

BAD_SRC="$(jq -r 'select(.header_update_source!=null) | .header_update_source' "$RUN_METRICS" | sort | uniq -c | awk '$2!="run_update"{print $2; exit}')"
if [ -z "$BAD_SRC" ]; then pass header_update_source; else fail header_update_source "Non-run_update source detected: $BAD_SRC"; fi

if pycheck signals_present; then pass signals_present; else fail signals_present "signals missing required keys"; fi

HAS_ZERO="$(jq -r 'select(.signals!=null) | .signals["EC_Identity.same"]' "$RUN_METRICS" | awk '$1==0{print; exit}')"
HAS_ONE="$(jq -r 'select(.signals!=null) | .signals["EC_Identity.same"]' "$RUN_METRICS" | awk '$1==1{print; exit}')"
HAS_LASTD="$(jq -r 'first(select(.signals!=null and (.signals["EC_Identity.last_d"]|tonumber)>0) | .t) // empty' "$RUN_METRICS")"
if [ -n "$HAS_ZERO" ] && [ -n "$HAS_ONE" ] && [ -n "$HAS_LASTD" ]; then pass identity_variation; else fail identity_variation "identity_ok not varying or last_d never > 0"; fi

HAS_BIRTH="$(jq -r 'first(select(.signals!=null and .signals["EB_GHVC.birth_suggest"]==1) | .t) // empty' "$RUN_METRICS")"
BIRTH_CHG="$(jq -r 'select(.birth_count!=null) | .birth_count' "$RUN_METRICS" | sort -n | uniq -c | wc -l | awk '$1>1{print}')"
if [ -n "$HAS_BIRTH" ] && [ -n "$BIRTH_CHG" ]; then pass ghvc_birth; else fail ghvc_birth "No birth_suggest==1 or birth_count not changing"; fi

BAD_MASK="$(jq -r 'select(.metric=="co_debug") | select(.translator_mask!=null and (.translator_mask|type=="array") and .action!=null) | (.mask_mode // "blocklist") as $mode | if $mode=="allowlist" then ((.translator_mask|index(.action))==null) elif $mode=="blocklist" then ((.translator_mask|index(.action))!=null) else false end | select(.) | .t' "$RUN_METRICS" | head -n 1)"
if [ -z "$BAD_MASK" ]; then pass mask_semantics; else fail mask_semantics "Mask contract violated at t=$BAD_MASK"; fi

BAD_T2="$(jq -r 'select(.metric=="co_debug") | .t' "$RUN_METRICS" | sort -n | uniq -c | awk '$1!=1{print $2}' | head -n 1)"
if [ -z "$BAD_T2" ]; then pass co_debug_once; else fail co_debug_once "co_debug count != 1 at t=$BAD_T2"; fi

echo
if [ "${#FAILS[@]}" -eq 0 ]; then
  echo "PASS: all checks"
  exit 0
else
  echo "FAIL: ${#FAILS[@]} check(s) failed -> ${FAILS[*]}"
  exit 1
fi
