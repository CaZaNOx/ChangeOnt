class C_ClassicOps:
    """Retired guard: non-CO operations are not part of the CO kernel.

    Keep this class only to make accidental imports fail explicitly. External
    baselines belong in experiment/study code, never as an in-kernel rescue path.
    """

    def __init__(self, *args, **kwargs):
        raise RuntimeError("C_ClassicOps is retired from the certified CO runtime")

    @staticmethod
    def add(xs):
        raise RuntimeError("C_ClassicOps is retired from the certified CO runtime")

    @staticmethod
    def mul(xs):
        raise RuntimeError("C_ClassicOps is retired from the certified CO runtime")
