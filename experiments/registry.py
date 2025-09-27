# experiments/registry.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Any, Callable


@dataclass(frozen=True)
class AgentSpec:
    """
    Family-specific description of how to encode an agent
    into the runner's config.
    - For bandit:      agent -> {"type": <runner_type>, "params": {...}}
    - For maze:        agent -> {"type": <"bfs"|"haq">, "params": {...}}
    - For renewal:     mode  -> <"last"|"ngram"|"phase"|"haq">, and optional params
    """
    family: str
    label: str
    builder: Callable[[Dict[str, Any]], Dict[str, Any]]  # takes selection params; returns dict for runner


# ---- BANDIT registry ----
def _bandit_ucb1(_sel: Dict[str, Any]) -> Dict[str, Any]:
    return {"type": "ucb1", "params": {}}

def _bandit_epsgreedy(sel: Dict[str, Any]) -> Dict[str, Any]:
    # allow simple override via selection (epsilon: 0.1 default)
    eps = float(sel.get("epsilon", 0.1))
    return {"type": "epsgreedy", "params": {"epsilon": eps}}

def _bandit_haq_base(sel: Dict[str, Any]) -> Dict[str, Any]:
    # Runner-side CO agent typically reads custom params if supported.
    # We pass a canonical ema_alpha; adjust here if you have variants.
    return {"type": "haq", "params": {"ema_alpha": float(sel.get("ema_alpha", 0.10))}}

def _bandit_haq_slow(sel: Dict[str, Any]) -> Dict[str, Any]:
    return {"type": "haq", "params": {"ema_alpha": 0.03}}

def _bandit_haq_fast(sel: Dict[str, Any]) -> Dict[str, Any]:
    return {"type": "haq", "params": {"ema_alpha": 0.30}}


BANDIT_AGENTS: Dict[str, AgentSpec] = {
    "ucb1":          AgentSpec("bandit", "ucb1", _bandit_ucb1),
    "epsgreedy":     AgentSpec("bandit", "epsgreedy", _bandit_epsgreedy),
    "co:haq_base":   AgentSpec("bandit", "co:haq_base", _bandit_haq_base),
    "co:haq_slowema":AgentSpec("bandit", "co:haq_slowema", _bandit_haq_slow),
    "co:haq_fastema":AgentSpec("bandit", "co:haq_fastema", _bandit_haq_fast),
}


# ---- MAZE registry ----
def _maze_bfs(_sel: Dict[str, Any]) -> Dict[str, Any]:
    return {"type": "bfs", "params": {}}

def _maze_haq(sel: Dict[str, Any]) -> Dict[str, Any]:
    # Example configurable knob for your HAQ maze agent (if supported)
    # e.g., L_hist via selection: {L_hist: 4}
    params = {}
    if "L_hist" in sel:
        params["L_hist"] = int(sel["L_hist"])
    return {"type": "haq", "params": params}

MAZE_AGENTS: Dict[str, AgentSpec] = {
    "stoa:bfs": AgentSpec("maze", "stoa:bfs", _maze_bfs),
    "co:haq_w4": AgentSpec("maze", "co:haq_w4", lambda _: _maze_haq({"L_hist": 4})),
    "co:haq":    AgentSpec("maze", "co:haq", _maze_haq),
}


# ---- RENEWAL registry ----
def _renewal_mode(mode: str) -> Callable[[Dict[str, Any]], Dict[str, Any]]:
    def _f(sel: Dict[str, Any]) -> Dict[str, Any]:
        # Renewal runner reads "mode": "last|ngram|phase|haq"
        # Optional CO params can be forwarded under "agent": {"params": {...}} if supported by your runner.
        out = {"mode": mode}
        if sel:
            out["agent"] = {"params": sel}  # harmless if runner ignores
        return out
    return _f

RENEWAL_AGENTS: Dict[str, AgentSpec] = {
    "stoa:last":  AgentSpec("renewal", "stoa:last",  _renewal_mode("last")),
    "stoa:ngram": AgentSpec("renewal", "stoa:ngram", _renewal_mode("ngram")),
    "stoa:phase": AgentSpec("renewal", "stoa:phase", _renewal_mode("phase")),
    "co:haq":     AgentSpec("renewal", "co:haq",     _renewal_mode("haq")),
    # Examples if you later expose HAQ knobs in runner config:
    # "co:haq_L6_e01": AgentSpec("renewal","co:haq_L6_e01", _renewal_mode("haq")),
}


# ---- Master registry ----
AGENT_REGISTRY: Dict[str, Dict[str, AgentSpec]] = {
    "bandit":  BANDIT_AGENTS,
    "maze":    MAZE_AGENTS,
    "renewal": RENEWAL_AGENTS,
}


def resolve_agent(family: str, label: str) -> AgentSpec:
    fam = AGENT_REGISTRY.get(family, {})
    if label not in fam:
        raise KeyError(f"Unknown agent label '{label}' for family '{family}'. "
                       f"Known: {list(fam.keys())}")
    return fam[label]
