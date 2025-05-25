from typing import Dict
from ..base import Organism
from constants.enums import CasteType
import random

class Cleaner(Organism):
    def __init__(self, organism_id: int, age: int = 0):
        super().__init__(CasteType.CLEANER, organism_id, age)
        
    def process_waste(self, waste_amount: int) -> Dict[str, int]:
        if not self.active:
            return {'waste_processed': 0, 'biomass_recycled': 0}
            
        effectiveness = self.get_effectiveness()
        processed = int(min(waste_amount, random.randint(8, 15)) * effectiveness)
        biomass_recycled = processed // 2
        
        return {
            'waste_processed': processed,
            'biomass_recycled': biomass_recycled
        }