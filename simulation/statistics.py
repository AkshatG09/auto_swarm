from typing import Dict, Any
from entities.hive_state import HiveState
from constants.enums import CasteType
from entities.base import Organism

def get_simulation_statistics(hive_state: HiveState, cycle_count: int) -> Dict[str, Any]:
    """Generate simulation statistics"""
    return {
        'total_cycles': cycle_count,
        'total_population': sum(hive_state.population.values()),
        'total_births': hive_state.total_births,
        'total_deaths': hive_state.total_deaths,
        'current_food': hive_state.food_level,
        'current_waste': hive_state.waste_level,
        'current_threat': hive_state.threat_level.name,
        'current_structure': hive_state.structural_integrity,
        'population_by_caste': {caste.value: count for caste, count in hive_state.population.items()}
    }

def print_status(hive_state: HiveState, organisms: Dict[int, 'Organism']):
    """Print current hive status"""
    total_population = sum(hive_state.population.values())
    living_queens = [org for org in organisms.values() 
                     if org.caste_type == CasteType.QUEEN and org.active]
    queen_info = f" (Queen: {living_queens[0].id}, age {living_queens[0].age})" if living_queens else " (NO QUEEN!)"
    
    print(f"Food: {hive_state.food_level} | "
          f"Waste: {hive_state.waste_level} | "
          f"Structure: {hive_state.structural_integrity}% | "
          f"Threat: {hive_state.threat_level.name}")
    
    print(f"Population ({total_population} total){queen_info}:", end=" ")
    for caste_type, count in hive_state.population.items():
        if count > 0:
            print(f"{caste_type.value}: {count}", end=" | ")
    print()
    
    print(f"Total Births: {hive_state.total_births} | Total Deaths: {hive_state.total_deaths}")