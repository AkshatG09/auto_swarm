from typing import Dict
from ..base import Organism
from constants.enums import CasteType, ThreatLevel
import random
from ..hive_state import HiveState

class Worker(Organism):
    def __init__(self, organism_id: int, age: int = 0):
        super().__init__(CasteType.WORKER, organism_id, age)
        
    def execute_tasks(self, hive_state: 'HiveState') -> Dict[str, int]:
        if not self.active:
            return {}
            
        results = {}
        effectiveness = self.get_effectiveness()
        food_gathered = int(random.randint(3, 8) * effectiveness)
        results['food_gathered'] = food_gathered
        
        detection_skill = 0.1 * effectiveness
        threat_detected = random.random() < detection_skill
        if threat_detected:
            results['threat_detected'] = random.choice([ThreatLevel.LOW, ThreatLevel.MEDIUM])
            
        results['waste_generated'] = random.randint(1, 3)
        return results