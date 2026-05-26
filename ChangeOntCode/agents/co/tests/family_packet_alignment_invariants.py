"""Invariant/diagnostic module for family packet alignment invariants.

Run with: python -m agents.co.tests.family_packet_alignment_invariants
"""
from __future__ import annotations

from agents.co.adapters.bandit_adapter import COAdapterBandit
from agents.co.adapters.latent_mechanism_adapter import COAdapterLatentMechanism
from agents.co.integration.core_builder import build_co_core


def _assert(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def _core():
    return build_co_core({"header": {"type": "SSI"}, "elements": {"candidate_surface": {"enabled": True}, "commitment_surface": {"enabled": True, "ngram_order": 0}}, "combinator": {"order": ["candidate_surface", "commitment_surface"]}, "primitives": {"signal_bus": {}, "bandit_stats": {}}})


def test_bandit_update_packet_preserves_goal_field_and_measurement_evidence() -> None:
    a = COAdapterBandit(_core(), n_arms=2)
    obs = {"t": 0, "rewards": [0.0, 0.0], "counts": [1, 2]}
    a.select(obs)
    packet = a._last_obs
    _assert(bool(packet.get("goal_field")), "bandit select packet should include goal_field")
    _assert(bool(packet.get("measurement_evidence")), "bandit select packet should include measurement_evidence")
    a.update({"action": 0, "reward": 1.0, "done": False})
    packet2 = a._last_obs
    _assert(bool(packet2.get("goal_field")), "bandit update packet should preserve goal_field")
    _assert(bool(packet2.get("measurement_evidence")), "bandit update packet should preserve measurement_evidence")


def test_latent_mechanism_select_packet_emits_measurement_evidence() -> None:
    a = COAdapterLatentMechanism(_core())
    obs = {
        "t": 0,
        "pos": (0, 0),
        "goal": (2, 2),
        "door": (1, 1),
        "switches": [(0, 1)],
        "decoys": [],
        "door_open": False,
        "hiddenness": 0.6,
        "rewrite_harshness": 0.5,
        "local_deceptiveness": 0.4,
        "legal_actions": ["UP", "RIGHT", "INTERACT"],
    }
    a.select(obs)
    packet = a._last_obs
    _assert(bool(packet.get("goal_field")), "latent mechanism packet should include goal_field")
    _assert(bool(packet.get("measurement_evidence")), "latent mechanism packet should include measurement_evidence")
