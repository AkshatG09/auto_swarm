from .enums import *

# Lifespan settings in cycles
LIFESPANS = {
    CasteType.QUEEN: 100,
    CasteType.WORKER: 25,
    CasteType.SOLDIER: 20,
    CasteType.CLEANER: 30,
    CasteType.BREEDER: 35,
    CasteType.BIO_ARCHITECT: 40
}

# Initial population counts
INITIAL_POPULATION = {
    CasteType.QUEEN: 1,
    CasteType.WORKER: 10,
    CasteType.SOLDIER: 5,
    CasteType.CLEANER: 3,
    CasteType.BREEDER: 2,
    CasteType.BIO_ARCHITECT: 2
}

# Initial hive state
INITIAL_HIVE_STATE = {
    'food_level': 100,
    'waste_level': 0,
    'threat_level': ThreatLevel.NONE,
    'structural_integrity': 100
}