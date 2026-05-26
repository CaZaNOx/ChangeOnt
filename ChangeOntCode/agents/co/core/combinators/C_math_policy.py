class C_MathPolicy:
    """Canonical math-policy tag.

    The evidence-bearing runtime does not route to a non-CO policy. External
    baselines must be run outside the CO kernel.
    """

    def __init__(self, policy: str = "co"):
        policy = str(policy or "co").lower()
        if policy != "co":
            raise ValueError("Certified CO runtime permits only math_policy='co'")
        self.policy = "co"

    def selected(self) -> str:
        return "co"
