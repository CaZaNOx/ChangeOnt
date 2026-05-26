from __future__ import annotations
from typing import Dict, Any, List, Tuple, Iterable, Optional
from dataclasses import dataclass
from agents.co.runtime.support.scope_keys import resolve_decision_scope


def _freeze(x: Any):
    if isinstance(x, dict):
        return tuple(sorted((str(k), _freeze(v)) for k, v in x.items()))
    if isinstance(x, (list, tuple)):
        return tuple(_freeze(v) for v in x)
    if isinstance(x, set):
        return tuple(sorted(_freeze(v) for v in x))
    return x


def _kgrams(seq: Tuple, k: int) -> List[Tuple]:
    out: List[Tuple] = []
    n = len(seq)
    for i in range(0, max(0, n - k + 1)):
        out.append(tuple(seq[i:i + k]))
    return out


@dataclass
class EI_ChangeOps:
    PRIMITIVE_DEPS = ("P10_ChangeOpsCore (optional)", "P12_ClosureQuotient (optional)", "history/state support")
    COMBINATOR_DEPS = ()
    FORMULA_STATUS = "working-minimal-plus"

    k: int = 3
    mdl_select: bool = False
    annotation_scale: float = 1.0
    min_support: int = 1
    pair_weight: float = 0.50
    proto_weight: float = 0.35
    closure_weight: float = 0.20

    def configure(self, params: Dict[str, Any], context: Dict[str, Any]):
        self.k = max(2, int(params.get("k", self.k)))
        self.mdl_select = bool(params.get("mdl_select", self.mdl_select))
        self.annotation_scale = float(params.get("annotation_scale", self.annotation_scale))
        self.min_support = max(1, int(params.get("min_support", self.min_support)))
        self.pair_weight = float(params.get("pair_weight", self.pair_weight))
        self.proto_weight = float(params.get("proto_weight", self.proto_weight))
        self.closure_weight = float(params.get("closure_weight", self.closure_weight))
        return self

    def _run_core(self, history: Tuple, p10: Any | None = None) -> Dict[str, Any]:
        if p10 is not None and hasattr(p10, "kgrams"):
            try:
                grams = list(p10.kgrams(list(history)))
            except Exception:
                grams = _kgrams(history, self.k)
        else:
            grams = _kgrams(history, self.k)
        motif_counts: Dict[Tuple, int] = {}
        for g in grams:
            motif_counts[g] = motif_counts.get(g, 0) + 1
        comp_counts: Dict[Tuple[Tuple, Tuple], int] = {}
        for i in range(len(grams) - 1):
            pair = (grams[i], grams[i + 1])
            comp_counts[pair] = comp_counts.get(pair, 0) + 1
        return {"grams": grams, "motif_counts": motif_counts, "comp_counts": comp_counts}

    def _closure_rep_map(self, p12: Any, p10: Any) -> Dict[int, int]:
        reps: Dict[int, int] = {}
        if p12 is None or p10 is None:
            return reps
        try:
            classes = getattr(p12, "classes", {}) or {}
            rep = getattr(p12, "rep", {}) or {}
            if not classes or not rep:
                return reps
            for class_id, members in classes.items():
                r = int(rep.get(class_id, class_id))
                for m in members:
                    reps[int(m)] = r
        except Exception:
            return {}
        return reps

    def _prototype_grams(self, p10: Any, p12: Any) -> List[Tuple[Tuple, float]]:
        out: List[Tuple[Tuple, float]] = []
        if p10 is None:
            return out
        rep_map = self._closure_rep_map(p12, p10)
        seen_rep_grams: set[Tuple[int, Tuple]] = set()
        for idx, proto in enumerate(getattr(p10, "prototypes", []) or []):
            try:
                trace = tuple(_freeze(v) for v in getattr(proto, "trace", ()))
            except Exception:
                continue
            grams = _kgrams(trace, self.k)
            rep = rep_map.get(int(getattr(proto, "id", idx)), int(getattr(proto, "id", idx)))
            for gram in grams:
                tag = (rep, gram)
                if tag in seen_rep_grams:
                    continue
                seen_rep_grams.add(tag)
                out.append((gram, self.closure_weight))
        return out

    def _derive_candidate_annotations(
        self,
        history: Tuple,
        action_space: Iterable[Any],
        core: Dict[str, Any],
        p10: Any | None,
        p12: Any | None,
    ) -> Tuple[Dict[Any, float], int, Dict[str, int]]:
        domain = list(action_space or [])
        if not domain:
            return {}, 0, {"direct": 0, "pair": 0, "proto": 0}
        domain_set = set(domain)
        if len(history) < max(1, self.k - 1):
            return {}, 0, {"direct": 0, "pair": 0, "proto": 0}

        suffix = tuple(history[-(self.k - 1):]) if self.k > 1 else tuple()
        scores: Dict[Any, float] = {}
        ops_applied = 0
        source_counts = {"direct": 0, "pair": 0, "proto": 0}

        # Direct lawful next-step continuations from observed k-grams.
        for gram, count in core.get("motif_counts", {}).items():
            if len(gram) != self.k:
                continue
            if self.k > 1 and tuple(gram[:-1]) != suffix:
                continue
            nxt = gram[-1]
            if nxt in domain_set and int(count) >= self.min_support:
                scores[nxt] = scores.get(nxt, 0.0) + float(count)
                ops_applied += 1
                source_counts["direct"] += 1

        # Ordered composition over adjacent k-grams using P10.compose when possible.
        for (g1, g2), count in core.get("comp_counts", {}).items():
            if self.k > 1 and tuple(g1[:-1]) != suffix:
                continue
            if p10 is not None and hasattr(p10, "compose"):
                try:
                    comp = p10.compose(tuple(g1), tuple(g2), lambda a, b: 0.0 if tuple(a) == tuple(b) else 1.0)
                except Exception:
                    comp = None
            else:
                comp = None
            if comp is None:
                comp = tuple(g1) + tuple(g2[1:])
            nxt = comp[-1] if comp else None
            if nxt in domain_set and int(count) >= self.min_support:
                scores[nxt] = scores.get(nxt, 0.0) + self.pair_weight * float(count)
                ops_applied += 1
                source_counts["pair"] += 1

        # Prototype-backed lawful compositions; closure quotient avoids duplicate inflation.
        for gram, wt in self._prototype_grams(p10, p12):
            if len(gram) != self.k:
                continue
            if self.k > 1 and tuple(gram[:-1]) != suffix:
                continue
            nxt = gram[-1]
            if nxt in domain_set:
                scores[nxt] = scores.get(nxt, 0.0) + self.proto_weight * float(wt)
                ops_applied += 1
                source_counts["proto"] += 1

        if not scores:
            return {}, ops_applied, source_counts
        maxv = max(scores.values())
        if maxv > 0:
            scores = {a: self.annotation_scale * (float(v) / float(maxv)) for a, v in scores.items()}
        return scores, ops_applied, source_counts

    def _publish_annotations(self, observation: Dict[str, Any], primitives: Dict[str, Any], ann: Dict[Any, float], header: Any) -> None:
        primitives["_ei_candidate_annotations"] = dict(ann)
        bus = primitives.get("signal_bus")
        if bus is not None and hasattr(bus, "publish"):
            scope_key = resolve_decision_scope(observation, primitives, header)
            for a, w in ann.items():
                try:
                    bus.publish(scope_key=scope_key, action=a, weight=float(w), channel="order", rationale="ei_change_ops", source="EI_ChangeOps")
                except Exception:
                    continue

    def update(self, observation: Dict[str, Any], primitives: Dict[str, Any], header: Any, feedback: Dict[str, Any] | None):
        eps = float(getattr(getattr(header, "state", object()), "eps_eff", 0.0))
        hist_src = observation.get("trace") or observation.get("history", ())
        hist = tuple(_freeze(v) for v in hist_src)
        p10 = primitives.get("p10", primitives.get("P10"))
        p12 = primitives.get("p12", primitives.get("P12"))
        out = self._run_core(hist, p10)
        if self.mdl_select and out["motif_counts"]:
            motifs = sorted(out["motif_counts"].items(), key=lambda kv: (-kv[1], len(kv[0])))
            out["selected_motifs"] = motifs[: max(1, min(self.k, len(motifs)))]
        action_space = observation.get("action_space") or []
        ann, ops_applied, src_counts = self._derive_candidate_annotations(hist, action_space, out, p10, p12)
        out["candidate_annotations"] = ann
        out["ops_applied"] = int(ops_applied)
        out["annotation_sources"] = dict(src_counts)
        out["eps"] = eps
        self._publish_annotations(observation, primitives, ann, header)
        return out

    def step(self, observation: Dict[str, Any], primitives: Dict[str, Any], header: Any, feedback: Dict[str, Any] | None):
        return self.update(observation, primitives, header, feedback)
