"""Code-vs-certified-docs pipeline compliance invariants.

These tests protect the certified execution loop:
Boundary/Adapter -> CandidateSurface -> RelationSurface/RCF/Certificate ->
CommitmentSurface exactly once as final readout, with fail-closed telemetry on
surface errors.
"""
from __future__ import annotations

from agents.co.core.combinators.C_pipeline import C_Pipeline
from agents.co.runtime.surfaces.commitment_surface import CommitmentSurface


class Recorder:
    PRIMITIVE_DEPS = ()
    COMBINATOR_DEPS = ()
    def __init__(self, name: str, log: list[str], *, fail_step: bool = False) -> None:
        self.name = name
        self.log = log
        self.fail_step = fail_step
    def update(self, observation, primitives, header, feedback):
        self.log.append(f"{self.name}.update")
        return {f"{self.name}_updated": True}
    def step(self, observation, primitives, header, feedback):
        self.log.append(f"{self.name}.step")
        if self.fail_step:
            raise RuntimeError("intentional step failure")
        return {f"{self.name}_stepped": True}
    def metrics(self):
        self.log.append(f"{self.name}.metrics")
        return {f"{self.name}_metrics": True}


class DummyCommitment(CommitmentSurface):
    def __init__(self, log: list[str]) -> None:
        super().__init__()
        self.log = log
    def update(self, *args, **kwargs):  # must not be called by C_Pipeline.run_update
        self.log.append("commit.update")
        return {"commit_update_called": True}
    def step(self, observation, primitives, header, feedback):
        self.log.append("commit.step")
        return {"action": "chosen", "co_policy": "kernel:commit", "co_evidence_valid_for_step": True}
    def metrics(self):
        self.log.append("commit.metrics")
        return {"commit_metrics": True}


def _assert(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def test_commitment_surface_runs_once_and_last_even_if_config_order_is_wrong() -> None:
    log: list[str] = []
    commit = DummyCommitment(log)
    early = Recorder("early", log)
    late = Recorder("late", log)
    out = C_Pipeline().run([early, commit, late], {}, None, {"x": 1}, None)
    _assert(out.get("action") == "chosen", out)
    _assert(log[-1] == "commit.step", f"CommitmentSurface must be last; log={log}")
    _assert(log.count("commit.step") == 1, f"CommitmentSurface must run exactly once; log={log}")
    _assert("commit.update" not in log, f"CommitmentSurface update must not run in decision pass; log={log}")
    _assert("commit.metrics" not in log, f"CommitmentSurface metrics must not run before readout; log={log}")


def test_update_pass_skips_commitment_surface() -> None:
    log: list[str] = []
    commit = DummyCommitment(log)
    early = Recorder("early", log)
    class Header:
        def update(self, obs):
            log.append("header.update")
            return {"header_updated": True}
    out = C_Pipeline().run_update([commit, early], {}, Header(), {"x": 1}, {"r": 0})
    _assert(out.get("header_updated") is True, out)
    _assert("commit.step" not in log and "commit.update" not in log and "commit.metrics" not in log, f"update pass must skip commitment surface; log={log}")
    _assert("early.update" in log and "early.metrics" in log, f"non-readout element should update; log={log}")


def test_surface_error_marks_step_non_evidential_without_rescue_action() -> None:
    log: list[str] = []
    bad = Recorder("bad", log, fail_step=True)
    out = C_Pipeline().run([bad], {}, None, {"x": 1}, None)
    _assert(out.get("engineering_safety_triggered") is True, out)
    _assert(out.get("co_evidence_valid_for_step") is False, out)
    _assert("action" not in out, f"surface error must not be rescued into action: {out}")


def test_commitment_surface_run_update_is_fail_closed_if_called_directly() -> None:
    try:
        CommitmentSurface().run_update([], {}, None, {}, None)
    except RuntimeError as exc:
        _assert("not part of the canonical runtime" in str(exc), str(exc))
    else:
        raise AssertionError("CommitmentSurface.run_update must fail closed if old callers invoke it")


def main() -> None:
    test_commitment_surface_runs_once_and_last_even_if_config_order_is_wrong()
    test_update_pass_skips_commitment_surface()
    test_surface_error_marks_step_non_evidential_without_rescue_action()
    test_commitment_surface_run_update_is_fail_closed_if_called_directly()


if __name__ == "__main__":
    main()
