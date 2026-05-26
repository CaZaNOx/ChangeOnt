"""Compatibility import for the canonical C_Pipeline runtime orchestrator."""

# ChangeOntCode\agents\co\core\pipeline.py
from __future__ import annotations
from typing import Any, Dict, List, Optional

from agents.co.core.contracts.placement_contract import export_runtime_contract

class COAgentCore:
    """
    Orchestrates header + elements + primitives. Safe no-throw step().
    Exposes a stable surface for adapters: step(observation, feedback) -> metrics dict.

    The runtime operates on bounded local unfolding rather than a hidden full
    world-state. If a kernel_substrate primitive is present, the pipeline updates
    it before and after the element pass.
    """
    def __init__(self,
                 header: Any,
                 elements: List[Any],
                 primitives: Dict[str, Any],
                 combinators: Dict[str, Any],
                 math_policy: str = "co",
                 name: str = "CO_core",
                 meta_header: Any = None,
                 runtime_contract: Optional[Dict[str, Any]] = None):
        self.header = header
        self.meta_header = meta_header
        self.elements = elements
        self.primitives = primitives
        self.combinators = combinators
        self.math_policy = math_policy
        self.name = name
        self.runtime_contract = export_runtime_contract(runtime_contract or {})
        self._step = 0

    def export_runtime_contract(self) -> Dict[str, Any]:
        return export_runtime_contract(self.runtime_contract)

    def step(self, observation: Optional[Dict[str, Any]] = None,
             feedback: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        self._step += 1
        obs = dict(observation or {})
        fb  = dict(feedback or {})
        if self.meta_header is not None:
            try:
                obs.setdefault("meta_header", self.meta_header.to_dict(obs))
            except Exception:
                pass

        # 1) bounded local substrate pre-update (if present)
        metrics: Dict[str, Any] = {"core": self.name, "step": self._step}
        try:
            setattr(self.header, "_primitives", self.primitives)
            setattr(self.header, "core", self)
        except Exception:
            pass
        substrate = self.primitives.get("kernel_substrate")
        if substrate is not None and hasattr(substrate, "pre_update"):
            try:
                snap = substrate.pre_update(obs, fb, self.header)
                if isinstance(snap, dict):
                    obs["_kernel_substrate"] = snap
            except Exception as ex:
                metrics["kernel_substrate_pre"] = "failed"
                metrics.setdefault("errors", []).append({"where": "kernel_substrate.pre_update", "err": repr(ex)})
                metrics["engineering_safety_triggered"] = True
                metrics["co_evidence_valid_for_step"] = False
                metrics["safety_kind"] = "surface_error"

        # 2) Pipeline execution via combinator (header update is owned by run_update)
        pipeline = self.combinators.get("pipeline")
        if pipeline is not None and hasattr(pipeline, "run"):
            try:
                if fb and hasattr(pipeline, "run_update"):
                    # update pass owns header.update when feedback is present
                    block_metrics = pipeline.run_update(self.elements, self.primitives, self.header, obs, fb)
                else:
                    block_metrics = pipeline.run(self.elements, self.primitives, self.header, obs, fb)
                if isinstance(block_metrics, dict):
                    metrics.update(block_metrics)
            except Exception as ex:
                metrics["pipeline"] = "failed"
                metrics.setdefault("errors", []).append({"where": "pipeline.run", "err": repr(ex)})
                metrics["engineering_safety_triggered"] = True
                metrics["co_evidence_valid_for_step"] = False
                metrics["safety_kind"] = "pipeline_error"


        # 2b) explicit remaining-burden support primitive (if present)
        p16 = self.primitives.get("P16") or self.primitives.get("remaining_burden")
        if p16 is not None and hasattr(p16, "update"):
            try:
                rb = p16.update(obs, self.primitives, self.header, fb)
                if isinstance(rb, dict):
                    metrics.update(rb)
            except Exception as ex:
                metrics["P16_RemainingBurden"] = "failed"
                metrics.setdefault("errors", []).append({"where": "P16.update", "err": repr(ex)})
                metrics["engineering_safety_triggered"] = True
                metrics["co_evidence_valid_for_step"] = False
                metrics["safety_kind"] = "surface_error"

        # 2c) bounded local substrate post-update (if present)
        if substrate is not None and hasattr(substrate, "post_update"):
            try:
                substrate.post_update(self.primitives, metrics)
            except Exception as ex:
                metrics["kernel_substrate_post"] = "failed"
                metrics.setdefault("errors", []).append({"where": "kernel_substrate.post_update", "err": repr(ex)})
                metrics["engineering_safety_triggered"] = True
                metrics["co_evidence_valid_for_step"] = False
                metrics["safety_kind"] = "surface_error"
        # 3) Math policy (recorded for downstream); certified runtime is CO-only.
        if str(self.math_policy).lower() != "co":
            metrics.setdefault("errors", []).append({"where": "math_policy", "err": "non_co_policy_requested"})
            metrics["engineering_safety_triggered"] = True
            metrics["co_evidence_valid_for_step"] = False
            metrics["safety_kind"] = "math_policy_violation"
        metrics["math_policy"] = "co"
        return metrics
