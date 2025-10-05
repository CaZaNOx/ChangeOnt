from __future__ import annotations

class AntiOracle:  
    """  
    Static checks / flags to ensure we do not smuggle oracles:  
    - no direct access to plant time index  
    - no renewal/lap flags  
    - no hidden counters from environment  
    This class carries only booleans that an agent/harness can set for audit.  
    """  
    def __init__(self):  
        self.read_plant_time = False  
        self.read_renewal_flag = False  
        self.read_hidden_counters = False

    def ok(self) -> bool:
        return not (self.read_plant_time or self.read_renewal_flag or self.read_hidden_counters)

    def report(self) -> str:
        flags = []
        if self.read_plant_time: flags.append("plant_time")
        if self.read_renewal_flag: flags.append("renewal_flag")
        if self.read_hidden_counters: flags.append("hidden_counters")
        return "OK" if not flags else ("FORBIDDEN: " + ",".join(flags))
