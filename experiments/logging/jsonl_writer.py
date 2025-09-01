from future import annotations  
import os, json  
from typing import Any, Dict

class JSONLWriter:  
    def init(self, path: str):  
        os.makedirs(os.path.dirname(path), exist_ok=True)  
        self._f = open(path, "w", encoding="utf-8")


    def write(self, row: Dict[str, Any]) -> None:
        self._f.write(json.dumps(row) + "\n")

    def close(self) -> None:
        try:
            self._f.close()
        except Exception:
            pass


----

from **future** import annotations  
import json  
import os  
from typing import Any, Dict

class JSONLWriter:  
"""  
Simple JSONL writer with two streams: steps and episodes.  
"""  
def **init**(self, steps_path: str, episodes_path: str):  
os.makedirs(os.path.dirname(steps_path), exist_ok=True)  
self.f_steps = open(steps_path, "w", encoding="utf-8")  
self.f_eps = open(episodes_path, "w", encoding="utf-8")

```
def write_step(self, rec: Dict[str, Any]) -> None:
    self.f_steps.write(json.dumps(rec) + "\n")

def write_episode(self, rec: Dict[str, Any]) -> None:
    self.f_eps.write(json.dumps(rec) + "\n")

def close(self) -> None:
    self.f_steps.close()
    self.f_eps.close()