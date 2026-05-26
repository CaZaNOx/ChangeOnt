from __future__ import annotations
from typing import Iterable, Any, Dict, List, Tuple
from collections import Counter
from statistics import mean
from ._shared import publish_signal


def _freeze(x: Any):
    if isinstance(x, dict):
        return tuple(sorted((str(k), _freeze(v)) for k, v in x.items()))
    if isinstance(x, (list, tuple)):
        return tuple(_freeze(v) for v in x)
    if isinstance(x, set):
        return tuple(sorted(_freeze(v) for v in x))
    return x


class EE_Compressibility:
    """
    Bounded doctrinal realization of selective retention under admissible loss.

    Rather than scoring raw description length, EE identifies locally recurrent motifs,
    builds a small closure-stable prototype family over chunked unfolding, and measures
    how much of the current local history can be retained under admissible deformation.
    """
    PRIMITIVE_DEPS = ("history/state support", "P1_BendMetric (optional)", "signal_bus (optional)")
    COMBINATOR_DEPS = ()
    FORMULA_STATUS = "bounded-doctrinal"

    def __init__(self, window: int = 32, chunk_size: int = 3, cluster_eps: float = 0.22):
        self.window = max(6, int(window))
        self.chunk_size = max(2, int(chunk_size))
        self.cluster_eps = max(0.05, float(cluster_eps))
        self._last: Dict[str, float] = {}

    def configure(self, params: Dict[str, Any], context: Dict[str, Any]):
        if params:
            self.window = max(6, int(params.get("window", self.window)))
            self.chunk_size = max(2, int(params.get("chunk_size", self.chunk_size)))
            self.cluster_eps = max(0.05, float(params.get("cluster_eps", self.cluster_eps)))
        return self

    def _window_tokens(self, seq: Iterable[Any]) -> List[Any]:
        return [_freeze(x) for x in list(seq)[-self.window:]]

    def _chunks(self, toks: List[Any]) -> List[Tuple[Any, ...]]:
        if len(toks) < self.chunk_size:
            return [tuple(toks)] if toks else []
        return [tuple(toks[i:i + self.chunk_size]) for i in range(max(1, len(toks) - self.chunk_size + 1))]

    def _bend(self, a: Iterable[Any], b: Iterable[Any], primitives: Dict[str, Any]) -> float:
        P1 = primitives.get("P1")
        if P1 is None:
            aa, bb = list(a), list(b)
            ln = max(1, max(len(aa), len(bb)))
            mism = sum(1 for x, y in zip(aa, bb) if x != y) + abs(len(aa) - len(bb))
            return float(mism) / float(ln)
        if hasattr(P1, "directional_bend"):
            return float(P1.directional_bend(list(a), list(b)))
        if hasattr(P1, "bend_distance"):
            return float(P1.bend_distance(list(a), list(b)))
        return 0.0

    def _cluster_chunks(self, chunks: List[Tuple[Any, ...]], primitives: Dict[str, Any]) -> List[List[Tuple[Any, ...]]]:
        clusters: List[List[Tuple[Any, ...]]] = []
        reps: List[Tuple[Any, ...]] = []
        for ch in chunks:
            best_idx = None
            best_d = None
            for i, rep in enumerate(reps):
                d = self._bend(ch, rep, primitives)
                if d <= self.cluster_eps and (best_d is None or d < best_d):
                    best_idx = i
                    best_d = d
            if best_idx is None:
                reps.append(ch)
                clusters.append([ch])
            else:
                clusters[best_idx].append(ch)
        return clusters

    def _motif_strength(self, toks: List[Any]) -> float:
        motifs = []
        for n in (2, 3):
            if len(toks) >= n:
                motifs.extend(tuple(toks[i:i+n]) for i in range(len(toks)-n+1))
        if not motifs:
            return 0.0
        counts = Counter(motifs)
        total = sum(counts.values())
        dominant = max(counts.values())
        variety = len(counts) / float(total)
        return max(0.0, min(1.0, (dominant / float(total)) * (1.0 - 0.5 * variety)))

    def _predict(self, seq: Iterable[Any], primitives: Dict[str, Any]) -> Dict[str, float]:
        toks = self._window_tokens(seq)
        n = len(toks)
        if n <= 1:
            return {
                "score": 0.0,
                "repeat_ratio": 0.0,
                "nontriviality": 0.0,
                "token_variety": float(n),
                "selective_retention": 0.0,
                "admissible_loss": 1.0,
                "closure_stability": 0.0,
            }

        chunks = self._chunks(toks)
        clusters = self._cluster_chunks(chunks, primitives)
        prototype_count = max(1, len(clusters))
        recurrence_ratio = 1.0 - (prototype_count / float(max(1, len(chunks))))
        motif_strength = self._motif_strength(toks)
        token_variety = len(set(toks)) / float(n)
        nontriviality = max(0.0, min(1.0, motif_strength * (1.0 - 0.5 * token_variety) + 0.25 * recurrence_ratio))

        losses: List[float] = []
        stabilities: List[float] = []
        for cl in clusters:
            rep = cl[0]
            ds = [self._bend(ch, rep, primitives) for ch in cl]
            avg_d = float(mean(ds)) if ds else 0.0
            losses.append(avg_d)
            stabilities.append(max(0.0, min(1.0, 1.0 - avg_d)))
        admissible_loss = max(0.0, min(1.0, float(mean(losses)) if losses else 1.0))
        closure_stability = max(0.0, min(1.0, float(mean(stabilities)) if stabilities else 0.0))
        selective_retention = max(
            0.0,
            min(
                1.0,
                0.45 * closure_stability + 0.30 * nontriviality + 0.25 * recurrence_ratio * (1.0 - admissible_loss),
            ),
        )
        score = selective_retention
        return {
            "score": float(score),
            "repeat_ratio": float(recurrence_ratio),
            "nontriviality": float(nontriviality),
            "token_variety": float(token_variety),
            "selective_retention": float(selective_retention),
            "admissible_loss": float(admissible_loss),
            "closure_stability": float(closure_stability),
        }

    def update(self, observation: Dict[str, Any], primitives: Dict[str, Any], header: Any, feedback: Dict[str, Any] | None):
        hist = observation.get("history", [])
        out = self._predict(hist, primitives)
        bus = primitives.get("signal_bus")
        publish_signal(bus, "EE_Compressibility.score", out["score"])
        publish_signal(bus, "EE_Compressibility.nontriviality", out["nontriviality"])
        publish_signal(bus, "EE_Compressibility.selective_retention", out["selective_retention"])
        publish_signal(bus, "EE_Compressibility.admissible_loss", out["admissible_loss"])
        publish_signal(bus, "EE_Compressibility.closure_stability", out["closure_stability"])
        # compatibility alias
        publish_signal(bus, "EE_Compressibility.compressibility", out["score"])
        self._last = out
        return out

    def step(self, observation: Dict[str, Any], primitives: Dict[str, Any], header: Any, feedback: Dict[str, Any] | None):
        return self.update(observation, primitives, header, feedback)

    def report(self) -> Dict[str, float]:
        return dict(self._last)
