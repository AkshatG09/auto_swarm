import random
from typing import Dict, List
from entities import Organism, HiveState
from constants.enums import CasteType, ThreatLevel
from entities.castes.queen import Queen

def handle_threat_events(hive_state: HiveState) -> None:
    """Handle random threat events"""
    if random.random() < 0.05:
        current_level = hive_state.threat_level.value
        if current_level < 4:
            new_level = min(4, current_level + 1)
            hive_state.threat_level = ThreatLevel(new_level)
            print(f"🚨 Threat level increased to {hive_state.threat_level.name}")
            
    elif random.random() < 0.1:
        current_level = hive_state.threat_level.value
        if current_level > 0:
            new_level = max(0, current_level - 1)
            hive_state.threat_level = ThreatLevel(new_level)
            print(f"✅ Threat level reduced to {hive_state.threat_level.name}")

def handle_natural_births(organisms: Dict[int, Organism], hive_state: HiveState, cycle_count: int, next_organism_id: int) -> int:
    """Handle natural birth events"""
    if random.random() < 0.1:
        breeders = [org for org in organisms.values() 
                   if org.caste_type == CasteType.BREEDER and org.active]
        if breeders:
            natural_orders = {CasteType.WORKER: 1}
            if random.random() < 0.3:
                caste_options = [CasteType.CLEANER, CasteType.SOLDIER]
                natural_orders[random.choice(caste_options)] = 1
            
            for breeder in breeders[:1]:
                new_organisms = breeder.spawn_organisms(natural_orders, cycle_count)
                if new_organisms:
                    for org in new_organisms:
                        organisms[next_organism_id] = org
                        org.id = next_organism_id
                        hive_state.population[org.caste_type] += 1
                        hive_state.total_births += 1
                        next_organism_id += 1
                    print(f"🌱 Natural births: {[f'{org.caste_type.value}-{org.id}' for org in new_organisms]}")
                    break
    return next_organism_id

def handle_emergency_queen_spawn(organisms: Dict[int, Organism], hive_state: HiveState, cycle_count: int, next_organism_id: int) -> int:
    """Handle emergency queen spawning"""
    living_queens = [org for org in organisms.values() 
                     if org.caste_type == CasteType.QUEEN and org.active]
    if not living_queens:
        print("🚨 EMERGENCY QUEEN SPAWN: Creating new queen to save the hive!")
        emergency_queen = Queen(next_organism_id, age=random.randint(15, 25))
        emergency_queen.birth_cycle = cycle_count
        organisms[next_organism_id] = emergency_queen
        hive_state.population[CasteType.QUEEN] = 1
        hive_state.total_births += 1
        next_organism_id += 1
    return next_organism_id