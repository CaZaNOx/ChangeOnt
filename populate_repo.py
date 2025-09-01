# PURPOSE: Safely populate only empty/whitespace-only files from payloads.
#          For non-empty targets, write <file>.proposed and <file>.diff
# USAGE:   python tools/populate_repo.py --dry-run  (preview)
#          python tools/populate_repo.py            (apply)
import argparse, hashlib, os, sys, difflib

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
PAYLOAD_ROOT = os.path.join(ROOT, "tools", "payloads")

def is_whitespace_only(path: str) -> bool:
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = f.read()
        return len(data.strip()) == 0
    except FileNotFoundError:
        return True
    except Exception:
        # If binary or unreadable as text, treat as non-empty
        return False

def sha256_bytes(b: bytes) -> str:
    h = hashlib.sha256()
    h.update(b)
    return h.hexdigest()

def read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8", newline="") as f:
        return f.read()

def write_text(path: str, text: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)

def unified_diff(old: str, new: str, a: str, b: str) -> str:
    return "".join(
        difflib.unified_diff(
            old.splitlines(keepends=True),
            new.splitlines(keepends=True),
            fromfile=a,
            tofile=b,
            n=3,
        )
    )

def iter_payload_files():
    for base, _, files in os.walk(PAYLOAD_ROOT):
        for fn in files:
            payload_path = os.path.join(base, fn)
            # target path mirrors repo root (strip tools/payloads/)
            rel = os.path.relpath(payload_path, PAYLOAD_ROOT)
            target_path = os.path.join(ROOT, rel)
            yield payload_path, target_path

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="Preview actions only")
    args = ap.parse_args()

    if not os.path.isdir(PAYLOAD_ROOT):
        print(f"[ERROR] Missing payload root: {PAYLOAD_ROOT}", file=sys.stderr)
        sys.exit(1)

    print(f"[INFO] Repo root:       {ROOT}")
    print(f"[INFO] Payload root:    {PAYLOAD_ROOT}")
    print(f"[INFO] Dry-run:         {args.dry_run}")
    print("-" * 72)

    any_changes = False
    for payload_path, target_path in iter_payload_files():
        payload_text = read_text(payload_path)
        payload_bytes = payload_text.encode("utf-8")
        payload_sha = sha256_bytes(payload_bytes)

        exists = os.path.exists(target_path)
        if not exists:
            action = "create"
            any_changes = True
            print(f"[CREATE] {os.path.relpath(target_path, ROOT)} (sha256:{payload_sha[:12]})")
            if not args.dry_run:
                write_text(target_path, payload_text)
            continue

        if is_whitespace_only(target_path):
            action = "populate"
            any_changes = True
            print(f"[POPULATE] {os.path.relpath(target_path, ROOT)} (sha256:{payload_sha[:12]})")
            if not args.dry_run:
                write_text(target_path, payload_text)
            continue

        # Non-empty: compare and, if different, write proposed + diff
        current_text = read_text(target_path)
        if current_text == payload_text:
            print(f"[IDENTICAL] {os.path.relpath(target_path, ROOT)}")
            continue

        # Different content
        any_changes = True
        proposed = target_path + ".proposed"
        diffpath = target_path + ".diff"
        diff = unified_diff(current_text, payload_text, target_path, proposed)
        print(f"[PROPOSED] {os.path.relpath(target_path, ROOT)} -> .proposed + .diff")
        if not args.dry_run:
            write_text(proposed, payload_text)
            write_text(diffpath, diff)

    print("-" * 72)
    if any_changes:
        print("[DONE] Populate pass complete. Review any *.proposed and *.diff before merging.")
    else:
        print("[OK] Nothing to change. All targets either identical or no payloads matched.")

if __name__ == "__main__":
    main()
