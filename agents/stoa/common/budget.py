from __future__ import annotations
from dataclasses import dataclass
from typing import TextIO, Optional
import csv


@dataclass
class BudgetRow:
    step: int
    flops_per_step: float
    params: int
    precision: str
    memory_bits: int = 0
    context_len: int = 0


class BudgetLedger:
    """
    Minimal compute ledger: append-only CSV with fixed columns.
    """
    def __init__(self, fp: TextIO):
        self._w = csv.writer(fp)
        self._w.writerow(["step", "flops_per_step", "params", "precision", "memory_bits", "context_len"])

    def log(self, row: BudgetRow) -> None:
        self._w.writerow([row.step, row.flops_per_step, row.params, row.precision, row.memory_bits, row.context_len])
