#!/usr/bin/env bash
set -euo pipefail

FAILS=()

fail() {
  local name="$1" msg="$2"
  echo "FAIL: $name"
  echo "  $msg"
  FAILS+=("$name")
}

pass() { echo "PASS: $1"; }

# 1) Static grep gates
GREP_MATCHES="$(rg -n 'primitives\["P10"\]|primitives\["P12"\]|identity_mem|update_from_primitives' ChangeOntCode/agents/co || true)"
if [ -n "$GREP_MATCHES" ]; then
  fail "static_grep" "Disallowed symbols found in kernel code."
  echo "$GREP_MATCHES"
else
  pass "static_grep"
fi

# 2) Runtime gate: latest metrics.jsonl containing co_debug
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
print(co_paths[-1] if co_paths else "")
PY
)"

echo "LATEST_METRICS=$LATEST_METRICS"
if [ -z "$LATEST_METRICS" ]; then
  fail "latest_metrics" "No metrics.jsonl with co_debug found."
else
  # require translator_mask field on maze co_debug lines if maze is present
  MAZE_MASK_CHECK="$(
  LATEST_METRICS="$LATEST_METRICS" python - <<'PY'
import json, os
path = os.environ.get("LATEST_METRICS", "")
if not path:
    print("SKIP")
    raise SystemExit(0)
maze_present = False
mask_field_seen = False
with open(path, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except Exception:
            continue
        if obj.get("metric") != "co_debug":
            continue
        co_policy = str(obj.get("co_policy", ""))
        agent = str(obj.get("agent", "")).lower()
        is_maze = co_policy.startswith("maze:") or ("maze" in agent) or ("episode" in obj)
        if is_maze:
            maze_present = True
        if "translator_mask" in obj:
            mask_field_seen = True
if maze_present and not mask_field_seen:
    print("FAIL")
else:
    print("OK")
PY
  )"
  if [ "$MAZE_MASK_CHECK" = "FAIL" ]; then
    fail "maze_translator_mask" "No translator_mask field found in maze co_debug; run maze smoke with CO_DEBUG_MASK=1 or ensure runners log translator_mask."
  else
    pass "maze_translator_mask"
  fi

  # check mask semantics
  BAD_LINE="$(
  LATEST_METRICS="$LATEST_METRICS" python - <<'PY'
import json, os, sys
path = os.environ.get("LATEST_METRICS", "")
if not path:
    print("")
    raise SystemExit(0)
with open(path, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except Exception:
            continue
        if obj.get("metric") != "co_debug":
            continue
        if "translator_mask" not in obj:
            continue
        mask = obj.get("translator_mask")
        if mask is None:
            continue
        try:
            mask_list = list(mask)
        except Exception:
            continue
        if not mask_list:
            continue
        action = obj.get("action")
        blocks_all = obj.get("translator_mask_blocks_all")
        if blocks_all == 1:
            # must explicitly flag; ok even if action in mask
            continue
        # blocks_all missing or not 1: action must not be masked
        if action in mask_list:
            print(line)
            sys.exit(0)
print("")
PY
  )"

  if [ -n "$BAD_LINE" ]; then
    fail "mask_blocks_all" "Action selected from translator_mask without blocks_all flag."
    echo "  Offending co_debug:"
    echo "  $BAD_LINE"
  else
    pass "mask_blocks_all"
  fi
fi

echo
if [ "${#FAILS[@]}" -eq 0 ]; then
  echo "PASS: all checks"
  exit 0
else
  echo "FAIL: ${#FAILS[@]} check(s) failed -> ${FAILS[*]}"
  exit 1
fi
