from typing import Dict, Any
from ..base import Organism
from constants.enums import CasteType, ThreatLevel
from ..hive_state import HiveState

class CerebralCaste(Organism):
    def __init__(self, organism_id: int, age: int = 0):
        super().__init__(CasteType.CEREBRAL, organism_id, age)
        
    def analyze_existential_threat(self, hive_state: 'HiveState') -> Dict[str, Any]:
        strategies = {}
        effectiveness = self.get_effectiveness()
        
        # Trigger emergency protocols earlier
        if hive_state.threat_level.value >= ThreatLevel.HIGH.value:  # Changed from EXISTENTIAL
            spawn_multiplier = max(1, int(effectiveness * 2))  # More aggressive
            strategies['emergency_spawn'] = {
                CasteType.SOLDIER: 15 * spawn_multiplier,  # Increased from 10
                CasteType.WORKER: 3 * spawn_multiplier  # Reduced from 5 (focus on defense)
            }
            # Add structural reinforcements
            if hive_state.structural_integrity < 70:
                strategies['emergency_spawn'][CasteType.BIO_ARCHITECT] = 2
        return strategies