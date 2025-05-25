from dataclasses import dataclass
from typing import Dict
from constants.enums import CasteType, ThreatLevel
from constants.settings import INITIAL_POPULATION, INITIAL_HIVE_STATE

@dataclass
class HiveState:
    food_level: int = INITIAL_HIVE_STATE['food_level']
    waste_level: int = INITIAL_HIVE_STATE['waste_level']
    threat_level: ThreatLevel = INITIAL_HIVE_STATE['threat_level']
    structural_integrity: int = INITIAL_HIVE_STATE['structural_integrity']
    population: Dict[CasteType, int] = None
    total_births: int = 0
    total_deaths: int = 0
    emergency_mode: bool = False
    last_threat_cycle: int = -100
    worker_shortage_cycles: int = 0
    
    def __post_init__(self):
        if self.population is None:
            self.population = INITIAL_POPULATION.copy()