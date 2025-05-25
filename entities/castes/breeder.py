from typing import Dict, List
from ..base import Organism
from constants.enums import CasteType
from ..castes.worker import Worker
from ..castes.soldier import Soldier
from ..castes.cleaner import Cleaner
from ..castes.bio_architect import BioArchitect
from ..castes.queen import Queen
import random

class Breeder(Organism):
    def __init__(self, organism_id: int, age: int = 0):
        super().__init__(CasteType.BREEDER, organism_id, age)
        self.breeding_cooldown = 0
        
    def spawn_organisms(self, genetic_instructions: Dict[CasteType, int], current_cycle: int, living_queens_count: int = 1) -> List[Organism]:
        if not self.active or self.breeding_cooldown > 0:
            if self.breeding_cooldown > 0:
                self.breeding_cooldown -= 1
            return []
            
        new_organisms = []
        organism_counter = 1000 + random.randint(1, 999)
        effectiveness = self.get_effectiveness()
        breeding_capacity = max(1, int(3 * effectiveness))
        total_to_spawn = min(breeding_capacity, sum(genetic_instructions.values()))
        
        spawned_count = 0
        for caste_type, count in genetic_instructions.items():
            if spawned_count >= total_to_spawn:
                break
            
            if caste_type == CasteType.QUEEN:
                if living_queens_count > 0:
                    print(f"👑 BLOCKED: Cannot spawn new queen while {living_queens_count} queen(s) still alive")
                    continue
                else:
                    print("👑 EMERGENCY SUCCESSION: Spawning new queen as hive is queenless!")
                
            actual_count = min(count, total_to_spawn - spawned_count)
            actual_count = max(0, int(actual_count * effectiveness))
            
            for _ in range(actual_count):
                new_org = None
                if caste_type == CasteType.WORKER:
                    new_org = Worker(organism_counter)
                elif caste_type == CasteType.SOLDIER:
                    new_org = Soldier(organism_counter)
                elif caste_type == CasteType.CLEANER:
                    new_org = Cleaner(organism_counter)
                elif caste_type == CasteType.BIO_ARCHITECT:
                    new_org = BioArchitect(organism_counter)
                elif caste_type == CasteType.QUEEN:
                    new_org = Queen(organism_counter)
                elif caste_type == CasteType.BREEDER:
                    new_org = Breeder(organism_counter)
                    
                if new_org:
                    new_org.birth_cycle = current_cycle
                    new_organisms.append(new_org)
                    organism_counter += 1
                    spawned_count += 1
        
        if new_organisms:
            self.breeding_cooldown = random.randint(1, 3)
                
        return new_organisms