class SC_WeightedSelection:
    """Retired guard.

    Direct weighted max-selection is not part of the certified CO readout. The
    active CommitmentSurface must use earned-collapse certificate structure.
    """

    def __init__(self, *args, **kwargs):
        raise RuntimeError("SC_WeightedSelection is retired from certified CO runtime")
