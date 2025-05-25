from typing import Dict, Any
from ..base import Organism
from constants.enums import CasteType
from ..hive_state import HiveState
from constants.enums import ThreatLevel

class Queen(Organism):
    def __init__(self, organism_id: int, age: int = 0):
        super().__init__(CasteType.QUEEN, organism_id, age)
        self.genetic_blueprints = {}
        
    def process_stimuli(self, hive_state: 'HiveState', living_queens_count: int = 1) -> Dict[str, Any]:
        if not self.active:
            return {}
            
        priorities = {}
        effectiveness = self.get_effectiveness()
        
        if hive_state.food_level < 30:
            priorities['increase_workers'] = int(3 * effectiveness)
        elif hive_state.food_level > 80:
            priorities['reduce_workers'] = 1
            
        if hive_state.waste_level > 70:
            priorities['increase_cleaners'] = int(2 * effectiveness)
            
        if hive_state.threat_level.value >= 2:
            priorities['increase_soldiers'] = int(hive_state.threat_level.value * effectiveness)
            
        if hive_state.structural_integrity < 50:
            priorities['increase_bio_architects'] = int(2 * effectiveness)
            
        total_population = sum(hive_state.population.values())
        if total_population < 20:
            priorities['increase_workers'] = priorities.get('increase_workers', 0) + 2
            priorities['increase_breeders'] = 1
            
        if living_queens_count == 0:
            priorities['increase_queens'] = 1
            print("👑 SUCCESSION TRIGGERED: No living queens, spawning successor!")
        elif self.age > self.max_lifespan * 0.9 and living_queens_count == 1:
            priorities['increase_queens'] = 1
            print(f"👑 SUCCESSION PREPARATION: Queen {self.id} preparing successor (age {self.age}/{self.max_lifespan})")

        # EMERGENCY POPULATION FIXES:
    # Critical worker shortage (below 20% of initial population)
        if hive_state.population[CasteType.WORKER] < 2:  # Absolute minimum
            priorities['emergency_workers'] = 3  # Max priority spawning
            print("🚨 EMERGENCY: Critical worker shortage detected!")
    
    # If total population is dangerously low (below 5 organisms)
        total_pop = sum(hive_state.population.values())
        if total_pop < 5:
            priorities['emergency_all'] = 1
            print("🚨 EMERGENCY: Population collapse imminent!")

        current_soldiers = hive_state.population.get(CasteType.SOLDIER, 0)

        if hive_state.threat_level.value >= ThreatLevel.MEDIUM.value:
            current_soldiers = hive_state.population[CasteType.SOLDIER]
        if current_soldiers == 0:
            priorities['emergency_soldiers'] = 3  # Immediate soldier spawn
            print("🚨 EMERGENCY: No soldiers during threat!")
        elif current_soldiers < 3:  # Minimum soldier threshold
            priorities['increase_soldiers'] = 3 - current_soldiers
    
        return priorities
    
    def generate_genetic_instructions(self, priorities: Dict[str, Any]) -> Dict[CasteType, int]:
        if not self.active:
            return {}
            
        spawn_orders = {}
        
        for priority, urgency in priorities.items():
            if urgency <= 0:
                continue
                
            if 'increase_workers' in priority:
                spawn_orders[CasteType.WORKER] = urgency
            elif 'increase_cleaners' in priority:
                spawn_orders[CasteType.CLEANER] = urgency
            elif 'increase_soldiers' in priority:
                spawn_orders[CasteType.SOLDIER] = urgency
            elif 'increase_bio_architects' in priority:
                spawn_orders[CasteType.BIO_ARCHITECT] = urgency
            elif 'increase_queens' in priority:
                spawn_orders[CasteType.QUEEN] = urgency
            elif 'increase_breeders' in priority:
                spawn_orders[CasteType.BREEDER] = urgency
            elif 'emergency_workers' in priority:
                spawn_orders[CasteType.WORKER] = max(3, urgency)  # Minimum 3 workers
            elif 'emergency_all' in priority:
            # Emergency baseline population
                spawn_orders.update({
                    CasteType.WORKER: 2,
                    CasteType.CLEANER: 1,
                    CasteType.SOLDIER: 1
                })

        return spawn_orders