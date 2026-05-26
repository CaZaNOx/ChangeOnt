"""Invariant wrapper for the small frozen empirical sanity smoke."""
from __future__ import annotations

from experiments.studies.frozen_empirical_sanity_smoke_v1 import main


def test_frozen_empirical_sanity_smoke_executes_without_errors() -> None:
    payload = main()
    assert payload["constants_frozen"] is True
    assert len(payload["maintenance_rows"]) == 18
    assert len(payload["latent_rows"]) == 3
    assert not any("error" in r for r in payload["maintenance_rows"])
    assert not any("error" in r for r in payload["latent_rows"])
