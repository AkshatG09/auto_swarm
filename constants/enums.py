from enum import Enum

class ThreatLevel(Enum):
    NONE = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    EXISTENTIAL = 4

class CasteType(Enum):
    QUEEN = "Queen"
    WORKER = "Worker"
    SOLDIER = "Soldier"
    CLEANER = "Cleaner"
    BREEDER = "Breeder"
    BIO_ARCHITECT = "Bio-Architect"
    CEREBRAL = "Cerebral"