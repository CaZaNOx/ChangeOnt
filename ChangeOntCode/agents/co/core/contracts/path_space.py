from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional

@dataclass
class PathSpaceFragment:
    family: str = ""
    now_ref: Optional[str] = None
    anchor_id: Optional[str] = None
    prior_refs: List[str] = field(default_factory=list)
    k_window: int = 1
    path_depth: int = 0
    realized_segment: List[Dict[str, Any]] = field(default_factory=list)
    branch_space: List[Dict[str, Any]] = field(default_factory=list)
    feedback_fragment: Dict[str, Any] = field(default_factory=dict)
    translator_info: Dict[str, Any] = field(default_factory=dict)
    structural_profiles: Dict[str, Any] = field(default_factory=dict)
    regime_profiles: Dict[str, Any] = field(default_factory=dict)
    meta_priors: Dict[str, Any] = field(default_factory=dict)
    continuation_surface: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d.setdefault("t", self.path_depth)
        if self.now_ref is None:
            d["now_ref"] = f"{self.family}:t{self.path_depth}" if self.family else None
        return d


def normalize_fragment(raw: Dict[str, Any] | None, *, family: str = "", k_window: int = 1) -> Dict[str, Any]:
    src = dict(raw or {})
    fam = str(src.get("family", family) or family)
    depth = int(src.get("path_depth", src.get("t", 0) or 0))
    frag = PathSpaceFragment(
        family=fam,
        now_ref=src.get("now_ref") or (f"{fam}:t{depth}" if fam else None),
        anchor_id=src.get("anchor_id") or src.get("now_ref") or (f"{fam}:anchor:{depth}" if fam else None),
        prior_refs=list(src.get("prior_refs") or []),
        k_window=int(src.get("k_window", k_window) or k_window),
        path_depth=depth,
        realized_segment=list(src.get("realized_segment") or []),
        branch_space=list(src.get("branch_space") or []),
        feedback_fragment=dict(src.get("feedback_fragment") or {}),
        translator_info=dict(src.get("translator_info") or {}),
        structural_profiles=dict(src.get("structural_profiles") or {}),
        regime_profiles=dict(src.get("regime_profiles") or {}),
        meta_priors=dict(src.get("meta_priors") or {}),
        continuation_surface=dict(src.get("continuation_surface") or {}),
    )
    out = frag.to_dict()
    # Preserve useful extra keys so callers don't lose context.
    for k, v in src.items():
        if k not in out:
            out[k] = v
    return out


def merge_fragments(previous: Dict[str, Any] | None, current: Dict[str, Any] | None, *, family: str = "") -> Dict[str, Any]:
    prev = normalize_fragment(previous or {}, family=family) if previous else {}
    cur = normalize_fragment(current or {}, family=family) if current else {}
    if not prev:
        return dict(cur)
    if not cur:
        return dict(prev)
    fam = str(cur.get("family") or prev.get("family") or family)
    realized = list(prev.get("realized_segment") or []) + list(cur.get("realized_segment") or [])
    if len(realized) > int(cur.get("k_window", prev.get("k_window", 1)) or 1) * 4:
        realized = realized[-int(cur.get("k_window", prev.get("k_window", 1)) or 1) * 4 :]
    out = normalize_fragment({
        **prev,
        **cur,
        "family": fam,
        "prior_refs": list(dict.fromkeys(list(prev.get("prior_refs") or []) + list(cur.get("prior_refs") or []))),
        "realized_segment": realized,
        "branch_space": list(cur.get("branch_space") or prev.get("branch_space") or []),
        "feedback_fragment": {**dict(prev.get("feedback_fragment") or {}), **dict(cur.get("feedback_fragment") or {})},
        "translator_info": {**dict(prev.get("translator_info") or {}), **dict(cur.get("translator_info") or {})},
        "structural_profiles": {**dict(prev.get("structural_profiles") or {}), **dict(cur.get("structural_profiles") or {})},
        "regime_profiles": {**dict(prev.get("regime_profiles") or {}), **dict(cur.get("regime_profiles") or {})},
        "meta_priors": {**dict(prev.get("meta_priors") or {}), **dict(cur.get("meta_priors") or {})},
        "continuation_surface": dict(cur.get("continuation_surface") or prev.get("continuation_surface") or {}),
    }, family=fam)
    return out
