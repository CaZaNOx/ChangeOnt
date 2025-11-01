# C_math_policy.py
class C_MathPolicy:
    """
    Record math policy selection (classical vs CO). This combinator is a tag holder
    that can later be queried by elements to adjust arithmetic behavior.
    """
    def __init__(self, policy: str = "co"):
        self.policy = policy

    def selected(self) -> str:
        return self.policy
