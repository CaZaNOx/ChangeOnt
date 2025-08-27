import json, io

class JSONLWriter:
    def __init__(self, path):
        self.path = path
        self.fh = None
    def __enter__(self):
        self.fh = io.open(self.path, "w", encoding="utf-8")
        return self
    def write(self, obj):
        self.fh.write(json.dumps(obj)+"\n")
    def __exit__(self, exc_type, exc, tb):
        if self.fh:
            self.fh.flush()
            self.fh.close()