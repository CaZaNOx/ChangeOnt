# agents/stoa/__init__.py
# Keep package import robust: only export names that exist in agent_fsm.
try:
    from .agent_fsm import BFSAgent, UCB1Agent  # legacy; may not exist
except Exception:
    BFSAgent = None  # type: ignore
    UCB1Agent = None  # type: ignore

# Strong finite baselines (may or may not be present depending on your file)
try:
    from .agent_fsm import LastFSM, PhaseFSM, NGramFSM  # preferred names
except Exception:
    LastFSM = None  # type: ignore
    PhaseFSM = None  # type: ignore
    NGramFSM = None  # type: ignore

__all__ = [
    n for n, v in {
        "BFSAgent": BFSAgent,
        "UCB1Agent": UCB1Agent,
        "LastFSM": LastFSM,
        "PhaseFSM": PhaseFSM,
        "NGramFSM": NGramFSM,
    }.items() if v is not None
]
