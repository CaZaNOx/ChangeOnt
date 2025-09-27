# Re-run all families and print hashes
python -m experiments.verify_cli --suite all --config experiments/configs/verify_all.yaml
Get-ChildItem outputs/verify_* -Recurse -Filter *.jsonl | Get-FileHash | Format-Table -AutoSize
