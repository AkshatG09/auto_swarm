from dataclasses import dataclass
from typing import Dict
from constants.enums import CasteType
from constants.settings import LIFESPANS
import random

@dataclass
class Organism:
    def __init__(self, caste_type: CasteType, organism_id: int, age: int = 0):
        self.caste_type = caste_type
        self.id = organism_id
        self.age = age
        self.max_lifespan = LIFESPANS[caste_type]
        self.active = True
        self.energy = 100
        self.birth_cycle = None
        
    def age_organism(self) -> bool:
        self.age += 1
        aging_factor = self.age / self.max_lifespan
        if aging_factor > 0.7:
            decline = (aging_factor - 0.7) * 100
            self.energy = max(20, 100 - decline)
        
        if self.age >= self.max_lifespan:
            self.active = False
            return False
            
        death_chance = 0.001 + (aging_factor * 0.01)
        if random.random() < death_chance:
            self.active = False
            return False
            
        return True
    
    def get_effectiveness(self) -> float:
        if not self.active:
            return 0.0
        
        aging_factor = self.age / self.max_lifespan
        if aging_factor <= 0.3:
            return 0.7 + (aging_factor / 0.3) * 0.3
        elif aging_factor <= 0.7:
            return 1.0
        else:
            decline = (aging_factor - 0.7) / 0.3
            return 1.0 - (decline * 0.4)
        
    def __repr__(self):
        status = "💀" if not self.active else f"({self.age}/{self.max_lifespan})"
        birth_info = f"[Born C{self.birth_cycle}]" if self.birth_cycle else ""
        return f"{self.caste_type.value}-{self.id}{status}{birth_info}"