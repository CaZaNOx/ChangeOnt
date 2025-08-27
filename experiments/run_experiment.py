import argparse, yaml, os, sys
from experiments.runners.renewal_runner import run_renewal

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True, help="YAML config path")
    args = ap.parse_args()

    with open(args.config, "r") as f:
        cfg = yaml.safe_load(f)

    os.makedirs("outputs", exist_ok=True)

    bench = cfg.get("benchmark", {}).get("name", "")
    if bench != "renewal_codebook":
        print(f"Unsupported benchmark: {bench}")
        sys.exit(2)

    run_renewal(cfg)

if __name__ == "__main__":
    main()