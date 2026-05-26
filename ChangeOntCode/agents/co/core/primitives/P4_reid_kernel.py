from __future__ import annotations

from collections import deque
from statistics import mean
from typing import Any, Callable, Deque, Dict, Iterable, Sequence, Tuple


def _clamp(x: float) -> float:
    return max(0.0, min(1.0, float(x)))


def _default_components(a: Sequence[Any], b: Sequence[Any], match_cost: Callable[[Tuple[Any, ...], Tuple[Any, ...]], float]) -> Dict[str, float]:
    d = _clamp(match_cost(tuple(a), tuple(b)))
    return {
        "preserved_mass": 1.0 - d,
        "altered_mass": d,
        "directional_burden": d,
        "insertion_cost": 0.0,
        "deletion_cost": 0.0,
        "substitution_cost": d,
    }


class ReIDKernel:
    """
    Stateful bounded realization of admissibility-first re-identification.

    The kernel maintains a rolling burden/admissibility band and scores a target
    trace against a reference or memory cohort under:
    - preserved vs altered structure
    - burden relative to learned admissible band
    - persistence / fracture memory
    """

    def __init__(self, epsilon: float = 0.20, window: int = 8, persistence_alpha: float = 0.25) -> None:
        self.epsilon = float(epsilon)
        self.window = max(2, int(window))
        self.persistence_alpha = _clamp(float(persistence_alpha))
        self._burden_hist: Deque[float] = deque(maxlen=self.window)
        self._preserved_hist: Deque[float] = deque(maxlen=self.window)
        self._fracture_hist: Deque[float] = deque(maxlen=self.window)
        self._state: Dict[str, float] = {
            "continuity_ema": 0.5,
            "fracture_ema": 0.5,
            "admissibility_ema": 0.5,
        }

    def _band(self) -> Tuple[float, float]:
        if not self._burden_hist:
            return self.epsilon, self.epsilon
        mu = mean(self._burden_hist)
        var = mean((b - mu) ** 2 for b in self._burden_hist) if len(self._burden_hist) > 1 else 0.0
        sigma = var ** 0.5
        # admissibility region widens a little when history is noisy, but stays bounded.
        soft = _clamp(mu + 0.75 * sigma)
        hard = _clamp(mu + 1.50 * sigma + 0.10)
        return max(self.epsilon, soft), max(self.epsilon, hard)

    def _score(self, components: Dict[str, float]) -> Dict[str, float]:
        preserved = _clamp(float(components.get("preserved_mass", 0.0)))
        altered = _clamp(float(components.get("altered_mass", 1.0 - preserved)))
        burden = _clamp(float(components.get("directional_burden", altered)))
        soft_band, hard_band = self._band()
        if burden <= soft_band:
            admissibility = 1.0
        elif burden >= hard_band:
            admissibility = 0.0
        else:
            admissibility = 1.0 - ((burden - soft_band) / max(1e-9, hard_band - soft_band))
        continuity = _clamp(0.55 * preserved + 0.25 * (1.0 - burden) + 0.20 * admissibility)
        fracture = _clamp(0.55 * altered + 0.30 * burden + 0.15 * (1.0 - admissibility))
        return {
            "continuity": continuity,
            "fracture": fracture,
            "admissibility": admissibility,
            "preserved": preserved,
            "altered": altered,
            "burden": burden,
        }

    def _update_state(self, score: Dict[str, float]) -> None:
        self._burden_hist.append(float(score["burden"]))
        self._preserved_hist.append(float(score["preserved"]))
        self._fracture_hist.append(float(score["fracture"]))
        a = self.persistence_alpha
        self._state["continuity_ema"] = _clamp((1.0 - a) * self._state["continuity_ema"] + a * score["continuity"])
        self._state["fracture_ema"] = _clamp((1.0 - a) * self._state["fracture_ema"] + a * score["fracture"])
        self._state["admissibility_ema"] = _clamp((1.0 - a) * self._state["admissibility_ema"] + a * score["admissibility"])

    def compare_pair(
        self,
        trace: Sequence[Any],
        reference_trace: Sequence[Any],
        match_cost: Callable[[Tuple[Any, ...], Tuple[Any, ...]], float],
        *,
        bend_components: Callable[[Sequence[Any], Sequence[Any]], Dict[str, float]] | None = None,
    ) -> Dict[str, float]:
        components = bend_components(trace, reference_trace) if callable(bend_components) else _default_components(trace, reference_trace, match_cost)
        score = self._score(components)
        self._update_state(score)
        continuity_conf = _clamp(0.60 * score["continuity"] + 0.40 * self._state["continuity_ema"])
        fracture_pressure = _clamp(0.60 * score["fracture"] + 0.40 * self._state["fracture_ema"])
        identity_admissibility = _clamp(0.65 * score["admissibility"] + 0.35 * self._state["admissibility_ema"])
        return {
            "continuity_conf": float(continuity_conf),
            "fracture_pressure": float(fracture_pressure),
            "identity_admissibility": float(identity_admissibility),
            "reid_frequency": float(identity_admissibility),
            "preserved_mass": float(score["preserved"]),
            "altered_mass": float(score["altered"]),
            "directional_burden": float(score["burden"]),
            "insertion_cost": float(components.get("insertion_cost", 0.0)),
            "deletion_cost": float(components.get("deletion_cost", 0.0)),
            "substitution_cost": float(components.get("substitution_cost", 0.0)),
        }

    def compare_memory(
        self,
        trace: Sequence[Any],
        references: Iterable[Sequence[Any]],
        match_cost: Callable[[Tuple[Any, ...], Tuple[Any, ...]], float],
        *,
        bend_components: Callable[[Sequence[Any], Sequence[Any]], Dict[str, float]] | None = None,
    ) -> Dict[str, float]:
        refs = [tuple(r) for r in references if r]
        if not refs:
            out = self.compare_pair(trace, trace, match_cost, bend_components=bend_components)
            out["reid_frequency"] = 0.0
            return out
        scored = [self.compare_pair(trace, ref, match_cost, bend_components=bend_components) for ref in refs]
        # choose the best admissible reference, but keep cohort statistics
        best = max(scored, key=lambda d: (d["identity_admissibility"], d["continuity_conf"], -d["fracture_pressure"]))
        admiss_freq = sum(1 for s in scored if s["identity_admissibility"] >= max(self.epsilon, 0.5)) / float(len(scored))
        best = dict(best)
        best["reid_frequency"] = float(admiss_freq)
        best["cohort_continuity"] = float(mean(s["continuity_conf"] for s in scored))
        best["cohort_fracture"] = float(mean(s["fracture_pressure"] for s in scored))
        return best

    def assess(
        self,
        stream: Iterable[Any],
        template: Iterable[Any],
        match_cost: Callable[[Tuple[Any, ...], Tuple[Any, ...]], float],
        *,
        mismatch_taper: float = 0.35,
        bend_components: Callable[[Sequence[Any], Sequence[Any]], Dict[str, float]] | None = None,
    ) -> Dict[str, float]:
        seq = tuple(stream)
        tmpl = tuple(template)
        out = self.compare_pair(seq, tmpl, match_cost, bend_components=bend_components)
        out["fracture_pressure"] = _clamp(out["fracture_pressure"] * (1.0 + float(mismatch_taper) * 0.10))
        return out


__all__ = ["ReIDKernel"]
