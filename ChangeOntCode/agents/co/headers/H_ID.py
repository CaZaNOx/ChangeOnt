from __future__ import annotations

from .H_common import BaseHeader

class HeaderID(BaseHeader):
    """Retired guard header outside the certified CO runtime.

    The certified canonical runtime uses HeaderSSI. External studies must not
    use this header as an in-kernel rescue route.
    """

    def __init__(self, *args, **kwargs):
        raise RuntimeError("H_ID is retired from the certified CO runtime; use HeaderSSI")
