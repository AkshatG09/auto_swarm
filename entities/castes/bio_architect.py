from ..base import Organism
from constants.enums import CasteType
import random

class BioArchitect(Organism):
    def __init__(self, organism_id: int, age: int = 0):
        super().__init__(CasteType.BIO_ARCHITECT, organism_id, age)
        
    def maintain_structure(self, current_integrity: int) -> int:
        if not self.active:
            return current_integrity
            
        effectiveness = self.get_effectiveness()
        repair_amount = int(random.randint(5, 12) * effectiveness)
        return min(100, current_integrity + repair_amount)