from ..base import Organism
from constants.enums import CasteType, ThreatLevel
import random

class Soldier(Organism):
    def __init__(self, organism_id: int, age: int = 0):
        super().__init__(CasteType.SOLDIER, organism_id, age)
        
    def defend_hive(self, threat_level: ThreatLevel) -> int:
        if not self.active or threat_level == ThreatLevel.NONE:
            return 0
            
        effectiveness = self.get_effectiveness()
        defense_power = int(random.randint(5, 15) * threat_level.value * effectiveness)
        return defense_power