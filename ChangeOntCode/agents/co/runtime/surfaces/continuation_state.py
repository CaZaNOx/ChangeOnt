"""Continuation-identity tracking for candidate rows across local runtime steps.

The tracker supports the branch-is-not-action rule by retaining pressure-signature
state rather than treating native action labels as sufficient identity.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, Hashable, Iterable, List, Mapping, Sequence, Tuple


def clamp01(x: Any, default: float = 0.0) -> float:
    try:
        v = float(x)
    except Exception:
        v = float(default)
    if v < 0.0:
        return 0.0
    if v > 1.0:
        return 1.0
    return v


def _key(value: Any) -> Hashable:
    try:
        hash(value)
        return value  # type: ignore[return-value]
    except Exception:
        return repr(value)


FORBIDDEN_LEAKAGE_STATUS = {"hidden", "oracle", "solver", "policy", "optimal", "dp", "baseline", "private"}
ALLOWED_PUBLIC_BASES = {
    "visible_observation",
    "public_history",
    "declared_transition_rule",
    "legal_constraint",
    "public_contract",
    "public_effect",
    "local_geometry",
}
DECISION_SLOT_OPS = {"decision_slot", "single_decision_slot", "slot", "compete", "competition"}
_OPERATION_ALIASES = {
    "relieves": "relieve",
    "relief": "relieve",
    "reduces": "reduce",
    "decrease": "reduce",
    "decreases": "reduce",
    "reveals": "reveal",
    "exposes": "expose",
    "resets": "reset",
    "cancels": "cancel",
    "buffers": "buffer",
    "absorbs": "absorb",
    "carries": "carry",
    "postpones": "postpone",
    "single_decision_slot": "decision_slot",
    "decision-slot": "decision_slot",
}


def _stable_text(value: Any, default: str = "") -> str:
    out = "" if value is None else str(value).strip().lower()
    return out if out else default


def _normalize_operation(value: Any) -> str:
    op = _stable_text(value, "unknown")
    return _OPERATION_ALIASES.get(op, op)


def _public_effects(value: Any) -> List[Mapping[str, Any]]:
    if isinstance(value, Mapping):
        return [value]
    if isinstance(value, Iterable) and not isinstance(value, (str, bytes)):
        return [v for v in value if isinstance(v, Mapping)]
    return []


def derive_continuation_memory_id(features: Mapping[str, Any]) -> Tuple[Hashable, str]:
    """Derive a first-pass multi-step continuation-memory key from public effects.

    This key is intentionally weaker than RelationSurface ``branch_id``.  It is
    used only for persistence memory before final branch/relation construction,
    so different action expressions that handle the same public burden domain can
    inherit prior continuation pressure without collapsing into one branch.

    Precedence:
      1. explicit continuation-memory/continuation/branch fields when already
         published by a lawful upstream surface;
      2. dominant public burden domain from public_effects;
      3. candidate_id/action fallback.

    The public burden-domain key ignores native action labels and operation names
    while retaining burden type, scope, and coupling/relation scope.  Thus a
    carry/reduce/buffer expression over the same public burden domain can share
    memory, but distinct burdens such as hiddenness vs degradation remain separate.
    """
    for field in ("continuation_memory_id", "continuation_id", "branch_id"):
        value = features.get(field)
        if value is not None:
            return _key(value), field

    chosen: Tuple[float, Tuple[str, str, str, str]] | None = None
    for raw in _public_effects(features.get("public_effects", features.get("burden_effects", features.get("effect_facts", [])))):
        leakage = _stable_text(raw.get("leakage_status", "public"), "public")
        basis = _stable_text(raw.get("public_basis", ""), "")
        if leakage in FORBIDDEN_LEAKAGE_STATUS or basis not in ALLOWED_PUBLIC_BASES:
            continue
        op = _normalize_operation(raw.get("operation", raw.get("op", raw.get("effect", "unknown"))))
        if op in DECISION_SLOT_OPS:
            continue
        burden_type = _stable_text(raw.get("burden_type", raw.get("type", raw.get("effect_type", ""))), "")
        relation_scope = _stable_text(raw.get("relation_scope", raw.get("resource", raw.get("resource_type", raw.get("scope", "")))), "")
        scope = _stable_text(raw.get("scope"), relation_scope or "candidate")
        coupling = _stable_text(raw.get("coupling"), relation_scope or scope or "uncoupled")
        domain = burden_type or relation_scope
        if not domain:
            continue
        magnitude = clamp01(raw.get("magnitude", raw.get("weight", 1.0)), 1.0)
        key_parts = ("public_continuation_domain", coupling, scope, domain)
        if chosen is None or magnitude > chosen[0]:
            chosen = (magnitude, key_parts)
    if chosen is not None:
        return _key("::".join(chosen[1])), "public_effect_domain"

    for field in ("candidate_id", "action"):
        value = features.get(field)
        if value is not None:
            return _key(value), field
    return "branch", "fallback"


@dataclass
class ContinuationState:
    """Bounded memory for a candidate continuation across recent updates."""

    continuation_id: Hashable
    age: int = 0
    support_ema: float = 0.0
    burden_ema: float = 0.0
    fracture_ema: float = 0.0
    uncertainty_ema: float = 0.0
    previous_support_ema: float = 0.0
    previous_burden_ema: float = 0.0
    previous_fracture_ema: float = 0.0

    def update(self, *, support: float, burden: float, fracture: float, uncertainty: float, alpha: float = 0.42) -> Dict[str, float]:
        a = clamp01(alpha, 0.42)
        support = clamp01(support)
        burden = clamp01(burden)
        fracture = clamp01(fracture)
        uncertainty = clamp01(uncertainty)
        if self.age <= 0:
            self.support_ema = support
            self.burden_ema = burden
            self.fracture_ema = fracture
            self.uncertainty_ema = uncertainty
        else:
            self.previous_support_ema = self.support_ema
            self.previous_burden_ema = self.burden_ema
            self.previous_fracture_ema = self.fracture_ema
            self.support_ema = (1.0 - a) * self.support_ema + a * support
            self.burden_ema = (1.0 - a) * self.burden_ema + a * burden
            self.fracture_ema = (1.0 - a) * self.fracture_ema + a * fracture
            self.uncertainty_ema = (1.0 - a) * self.uncertainty_ema + a * uncertainty
        self.age += 1
        support_drop = max(0.0, self.previous_support_ema - self.support_ema) if self.age > 1 else 0.0
        burden_growth = max(0.0, self.burden_ema - self.previous_burden_ema) if self.age > 1 else 0.0
        fracture_growth = max(0.0, self.fracture_ema - self.previous_fracture_ema) if self.age > 1 else 0.0
        burden_accumulation = clamp01(0.60 * self.burden_ema + 0.25 * burden_growth + 0.15 * self.fracture_ema)
        instability = clamp01(0.38 * burden_accumulation + 0.28 * fracture_growth + 0.20 * support_drop + 0.14 * self.uncertainty_ema)
        persistence = clamp01(0.60 * self.support_ema + 0.20 * (1.0 - support_drop) + 0.20 * (1.0 - self.uncertainty_ema))
        viability = clamp01(0.52 * persistence + 0.22 * (1.0 - burden_accumulation) + 0.14 * (1.0 - self.fracture_ema) + 0.12 * (1.0 - instability))
        return {
            "continuation_age": float(self.age),
            "support_persistence": persistence,
            "burden_accumulation": burden_accumulation,
            "burden_trend": clamp01(burden_growth * 2.5),
            "fracture_trend": clamp01(fracture_growth * 2.5),
            "support_decay": clamp01(support_drop * 2.5),
            "continuation_instability": instability,
            "continuation_viability": viability,
            "support_ema": clamp01(self.support_ema),
            "burden_ema": clamp01(self.burden_ema),
            "fracture_ema": clamp01(self.fracture_ema),
        }

    def snapshot(self) -> Dict[str, Any]:
        return asdict(self)


class ContinuationStateTracker:
    """Bounded per-candidate continuation memory for runtime surfaces."""

    def __init__(self, max_entries: int = 256, alpha: float = 0.42) -> None:
        self.max_entries = max(1, int(max_entries))
        self.alpha = clamp01(alpha, 0.42)
        self._states: Dict[Hashable, ContinuationState] = {}
        self._tick = 0
        self._last_seen: Dict[Hashable, int] = {}

    def update_candidate(self, continuation_id: Any, features: Dict[str, Any]) -> Dict[str, float]:
        """Update one continuation-memory entry.

        Kept for compatibility.  New candidate publication should prefer
        ``update_candidate_batch`` so multiple action expressions that share one
        public continuation domain update memory once per runtime step.
        """
        return self.update_candidate_batch([(continuation_id, features)])[0]

    def update_candidate_batch(self, items: Sequence[Tuple[Any, Mapping[str, Any]]]) -> List[Dict[str, float]]:
        """Update continuation memory once per public continuation domain.

        CandidateSurface publishes several action expressions per decision.  If
        two expressions share the same public continuation-memory key, updating
        the EMA once for each expression would artificially age/amplify that
        continuation inside a single step.  This batch method aggregates rows by
        memory key, performs one update per key, and returns the same memory
        snapshot to all current expressions that share the key.
        """
        grouped: Dict[Hashable, List[Mapping[str, Any]]] = {}
        order: List[Hashable] = []
        for continuation_id, features in items:
            key = _key(continuation_id)
            grouped.setdefault(key, []).append(features)
            order.append(key)

        updated: Dict[Hashable, Dict[str, float]] = {}
        for key, vals in grouped.items():
            if key not in self._states:
                self._states[key] = ContinuationState(continuation_id=key)
            self._tick += 1
            self._last_seen[key] = self._tick
            support = sum(clamp01(v.get("support", v.get("support_mass", 0.0))) for v in vals) / float(len(vals) or 1)
            burden = max(clamp01(v.get("burden", v.get("burden_pressure", 0.0))) for v in vals)
            fracture = max(clamp01(v.get("fracture", v.get("fracture_state", 0.0))) for v in vals)
            uncertainty = max(clamp01(v.get("uncertainty", 0.0)) for v in vals)
            out = self._states[key].update(
                support=support,
                burden=burden,
                fracture=fracture,
                uncertainty=uncertainty,
                alpha=self.alpha,
            )
            out["continuation_memory_shared_count"] = float(len(vals))
            updated[key] = out
        self._evict_if_needed()
        return [dict(updated[k]) for k in order]

    def _evict_if_needed(self) -> None:
        if len(self._states) <= self.max_entries:
            return
        overflow = len(self._states) - self.max_entries
        old = sorted(self._last_seen.items(), key=lambda kv: kv[1])[:overflow]
        for key, _ in old:
            self._states.pop(key, None)
            self._last_seen.pop(key, None)

    def snapshots(self) -> Dict[str, Dict[str, Any]]:
        return {str(k): v.snapshot() for k, v in self._states.items()}
