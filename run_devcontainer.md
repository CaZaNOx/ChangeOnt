code ~/work/ChangeOnt

# 2.1 DRY-RUN from WSL → Drive (no changes, just report)
rsync -a --delete --dry-run ~/work/ChangeOnt/ "/mnt/g/My Drive/ChangeOntology/ChangeOnt/"

# 2.2 DRY-RUN from Drive → WSL (no changes)
rsync -a --delete --dry-run "/mnt/g/My Drive/ChangeOntology/ChangeOnt/" ~/work/ChangeOnt/

# 2.3 One real file push to Drive (safe test: the sentinel)
rsync -a ~/work/ChangeOnt/.container_sentinel.txt "/mnt/g/My Drive/ChangeOntology/ChangeOnt/"

# 2.4 See it on Drive
ls -l "/mnt/g/My Drive/ChangeOntology/ChangeOnt/.container_sentinel.txt"


$src = "\\wsl.localhost\Ubuntu-24.04\home\caza\work\ChangeOnt\"
$dst = "G:\My Drive\ChangeOntology\ChangeOnt\"
robocopy $src $dst * /MIR /FFT /XD ".git",".venv" /R:1 /W:1
