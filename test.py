import random
import time
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Optional
import threading

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

@dataclass
class HiveState:
    food_level: int = 100
    waste_level: int = 0
    threat_level: ThreatLevel = ThreatLevel.NONE
    structural_integrity: int = 100
    population: Dict[CasteType, int] = None
    total_births: int = 0  # Track total births
    total_deaths: int = 0  # Track total deaths
    
    def __post_init__(self):
        if self.population is None:
            self.population = {
                CasteType.QUEEN: 1,
                CasteType.WORKER: 10,
                CasteType.SOLDIER: 5,
                CasteType.CLEANER: 3,
                CasteType.BREEDER: 2,
                CasteType.BIO_ARCHITECT: 2,
                CasteType.CEREBRAL: 0
            }

class Organism:
    # Lifespan definitions for each caste (in cycles)
    LIFESPANS = {
        CasteType.QUEEN: 100,        # Long-lived leaders
        CasteType.WORKER: 25,        # Medium lifespan workhorses
        CasteType.SOLDIER: 20,       # Shorter due to combat stress
        CasteType.CLEANER: 30,       # Slightly longer than soldiers
        CasteType.BREEDER: 35,       # Need time to reproduce
        CasteType.BIO_ARCHITECT: 40, # Specialized, longer-lived
        CasteType.CEREBRAL: 50       # Valuable intelligence, protected
    }
    
    def __init__(self, caste_type: CasteType, organism_id: int, age: int = 0):
        self.caste_type = caste_type
        self.id = organism_id
        self.age = age
        self.max_lifespan = self.LIFESPANS[caste_type]
        self.active = True
        self.energy = 100
        self.birth_cycle = None  # Track when this organism was born
        
    def age_organism(self) -> bool:
        """Age the organism by one cycle. Returns True if still alive, False if died"""
        self.age += 1
        
        # Calculate aging effects on energy and effectiveness
        aging_factor = self.age / self.max_lifespan
        if aging_factor > 0.7:  # Start declining after 70% of lifespan
            decline = (aging_factor - 0.7) * 100
            self.energy = max(20, 100 - decline)
        
        # Death from old age
        if self.age >= self.max_lifespan:
            self.active = False
            return False
            
        # Small chance of early death due to various factors
        death_chance = 0.001 + (aging_factor * 0.01)  # Increases with age
        if random.random() < death_chance:
            self.active = False
            return False
            
        return True
    
    def get_effectiveness(self) -> float:
        """Get current effectiveness based on age (0.0 to 1.0)"""
        if not self.active:
            return 0.0
        
        aging_factor = self.age / self.max_lifespan
        if aging_factor <= 0.3:  # Young and growing
            return 0.7 + (aging_factor / 0.3) * 0.3  # 0.7 to 1.0
        elif aging_factor <= 0.7:  # Prime years
            return 1.0
        else:  # Declining years
            decline = (aging_factor - 0.7) / 0.3
            return 1.0 - (decline * 0.4)  # 1.0 to 0.6
        
    def __repr__(self):
        status = "💀" if not self.active else f"({self.age}/{self.max_lifespan})"
        birth_info = f"[Born C{self.birth_cycle}]" if self.birth_cycle else ""
        return f"{self.caste_type.value}-{self.id}{status}{birth_info}"

class Queen(Organism):
    def __init__(self, organism_id: int, age: int = 0):
        super().__init__(CasteType.QUEEN, organism_id, age)
        self.genetic_blueprints = {}
        
    def process_stimuli(self, hive_state: HiveState, living_queens_count: int = 1) -> Dict[str, any]:
        """Process internal and external stimuli to determine hive needs"""
        if not self.active:
            return {}
            
        priorities = {}
        effectiveness = self.get_effectiveness()
        
        # Analyze food situation (effectiveness affects decision quality)
        if hive_state.food_level < 30:
            priorities['increase_workers'] = int(3 * effectiveness)
        elif hive_state.food_level > 80:
            priorities['reduce_workers'] = 1
            
        # Analyze waste situation
        if hive_state.waste_level > 70:
            priorities['increase_cleaners'] = int(2 * effectiveness)
            
        # Analyze threat situation
        if hive_state.threat_level.value >= 2:
            priorities['increase_soldiers'] = int(hive_state.threat_level.value * effectiveness)
            
        # Analyze structural needs
        if hive_state.structural_integrity < 50:
            priorities['increase_bio_architects'] = int(2 * effectiveness)
            
        # Population management - encourage breeding when population is low
        total_population = sum(hive_state.population.values())
        if total_population < 20:
            priorities['increase_workers'] = priorities.get('increase_workers', 0) + 2
            priorities['increase_breeders'] = 1
            
        # MODIFIED: Only spawn new queen if there are NO living queens (succession)
        if living_queens_count == 0:
            priorities['increase_queens'] = 1
            print("👑 SUCCESSION TRIGGERED: No living queens, spawning successor!")
        elif self.age > self.max_lifespan * 0.9 and living_queens_count == 1:
            # Only prepare succession when very close to death and we're the only queen
            priorities['increase_queens'] = 1
            print(f"👑 SUCCESSION PREPARATION: Queen {self.id} preparing successor (age {self.age}/{self.max_lifespan})")
            
        return priorities
    
    def generate_genetic_instructions(self, priorities: Dict[str, any]) -> Dict[CasteType, int]:
        """Generate genetic blueprints for new organisms"""
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
                
        return spawn_orders

class Worker(Organism):
    def __init__(self, organism_id: int, age: int = 0):
        super().__init__(CasteType.WORKER, organism_id, age)
        
    def execute_tasks(self, hive_state: HiveState) -> Dict[str, int]:
        """Execute general tasks and gather environmental information"""
        if not self.active:
            return {}
            
        results = {}
        effectiveness = self.get_effectiveness()
        
        # Gather food (effectiveness affects productivity)
        food_gathered = int(random.randint(3, 8) * effectiveness)
        results['food_gathered'] = food_gathered
        
        # Detect environmental changes (experience helps with detection)
        detection_skill = 0.1 * effectiveness
        threat_detected = random.random() < detection_skill
        if threat_detected:
            results['threat_detected'] = random.choice([ThreatLevel.LOW, ThreatLevel.MEDIUM])
            
        # Generate some waste
        results['waste_generated'] = random.randint(1, 3)
        
        return results

class Soldier(Organism):
    def __init__(self, organism_id: int, age: int = 0):
        super().__init__(CasteType.SOLDIER, organism_id, age)
        
    def defend_hive(self, threat_level: ThreatLevel) -> int:
        """React to threats and engage intruders"""
        if not self.active or threat_level == ThreatLevel.NONE:
            return 0
            
        effectiveness = self.get_effectiveness()
        defense_power = int(random.randint(5, 15) * threat_level.value * effectiveness)
        return defense_power

class Cleaner(Organism):
    def __init__(self, organism_id: int, age: int = 0):
        super().__init__(CasteType.CLEANER, organism_id, age)
        
    def process_waste(self, waste_amount: int) -> Dict[str, int]:
        """Consume waste and recycle biomass"""
        if not self.active:
            return {'waste_processed': 0, 'biomass_recycled': 0}
            
        effectiveness = self.get_effectiveness()
        processed = int(min(waste_amount, random.randint(8, 15)) * effectiveness)
        biomass_recycled = processed // 2
        
        return {
            'waste_processed': processed,
            'biomass_recycled': biomass_recycled
        }

class Breeder(Organism):
    def __init__(self, organism_id: int, age: int = 0):
        super().__init__(CasteType.BREEDER, organism_id, age)
        self.breeding_cooldown = 0  # Prevent excessive breeding
        
    def spawn_organisms(self, genetic_instructions: Dict[CasteType, int], current_cycle: int, living_queens_count: int = 1) -> List[Organism]:
        """Create new organisms based on genetic instructions"""
        if not self.active or self.breeding_cooldown > 0:
            if self.breeding_cooldown > 0:
                self.breeding_cooldown -= 1
            return []
            
        new_organisms = []
        organism_counter = 1000 + random.randint(1, 999)  # Avoid ID conflicts
        effectiveness = self.get_effectiveness()
        
        # Reduce breeding capacity based on age and energy
        breeding_capacity = max(1, int(3 * effectiveness))
        total_to_spawn = min(breeding_capacity, sum(genetic_instructions.values()))
        
        spawned_count = 0
        for caste_type, count in genetic_instructions.items():
            if spawned_count >= total_to_spawn:
                break
            
            # MODIFIED: Special handling for queens - only spawn if no living queens exist
            if caste_type == CasteType.QUEEN:
                if living_queens_count > 0:
                    print(f"👑 BLOCKED: Cannot spawn new queen while {living_queens_count} queen(s) still alive")
                    continue  # Skip queen spawning if any queens are alive
                else:
                    print("👑 EMERGENCY SUCCESSION: Spawning new queen as hive is queenless!")
                
            # Effectiveness affects breeding success
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
                    new_org.birth_cycle = current_cycle  # Track birth cycle
                    new_organisms.append(new_org)
                    organism_counter += 1
                    spawned_count += 1
        
        # Set breeding cooldown if organisms were spawned
        if new_organisms:
            self.breeding_cooldown = random.randint(1, 3)
                
        return new_organisms

class BioArchitect(Organism):
    def __init__(self, organism_id: int, age: int = 0):
        super().__init__(CasteType.BIO_ARCHITECT, organism_id, age)
        
    def maintain_structure(self, current_integrity: int) -> int:
        """Adapt structure and regulate environment"""
        if not self.active:
            return current_integrity
            
        effectiveness = self.get_effectiveness()
        repair_amount = int(random.randint(5, 12) * effectiveness)
        return min(100, current_integrity + repair_amount)

class CerebralCaste(Organism):
    def __init__(self, organism_id: int, age: int = 0):
        super().__init__(CasteType.CEREBRAL, organism_id, age)
        
    def analyze_existential_threat(self, hive_state: HiveState) -> Dict[str, any]:
        """Process complex threats and formulate strategies"""
        if not self.active:
            return {}
            
        strategies = {}
        effectiveness = self.get_effectiveness()
        
        if hive_state.threat_level == ThreatLevel.EXISTENTIAL:
            spawn_multiplier = max(1, int(effectiveness * 1.5))
            strategies['emergency_spawn'] = {
                CasteType.SOLDIER: 10 * spawn_multiplier,
                CasteType.WORKER: 5 * spawn_multiplier
            }
            strategies['emergency_protocols'] = [
                'reduce_energy_consumption',
                'increase_structural_defenses',
                'prepare_evacuation_routes'
            ]
            
        return strategies

class HiveSimulation:
    def __init__(self):
        self.hive_state = HiveState()
        self.organisms = {}
        self.cycle_count = 0
        self.running = False
        self.next_organism_id = 1000  # Start IDs from 1000 to avoid conflicts
        
        # Initialize organisms
        self._initialize_organisms()
        
    def _initialize_organisms(self):
        """Initialize the starting population"""
        organism_id = 1
        
        # Queens - start with exactly 1
        for _ in range(self.hive_state.population[CasteType.QUEEN]):
            # Start with mature queens
            self.organisms[organism_id] = Queen(organism_id, age=random.randint(20, 40))
            organism_id += 1
            
        # Workers
        for _ in range(self.hive_state.population[CasteType.WORKER]):
            self.organisms[organism_id] = Worker(organism_id, age=random.randint(0, 15))
            organism_id += 1
            
        # Soldiers
        for _ in range(self.hive_state.population[CasteType.SOLDIER]):
            self.organisms[organism_id] = Soldier(organism_id, age=random.randint(0, 12))
            organism_id += 1
            
        # Cleaners
        for _ in range(self.hive_state.population[CasteType.CLEANER]):
            self.organisms[organism_id] = Cleaner(organism_id, age=random.randint(0, 18))
            organism_id += 1
            
        # Breeders
        for _ in range(self.hive_state.population[CasteType.BREEDER]):
            self.organisms[organism_id] = Breeder(organism_id, age=random.randint(5, 20))
            organism_id += 1
            
        # Bio-Architects
        for _ in range(self.hive_state.population[CasteType.BIO_ARCHITECT]):
            self.organisms[organism_id] = BioArchitect(organism_id, age=random.randint(0, 25))
            organism_id += 1
        
        self.next_organism_id = organism_id
    
    def _get_organisms_by_caste(self, caste_type: CasteType) -> List[Organism]:
        """Get all living organisms of a specific caste type"""
        return [org for org in self.organisms.values() 
                if org.caste_type == caste_type and org.active]
    
    def _age_all_organisms(self) -> Dict[str, int]:
        """Age all organisms and remove the dead ones"""
        deaths = {}
        dead_organisms = []
        queen_died = False
        
        for org_id, organism in self.organisms.items():
            if organism.active:
                still_alive = organism.age_organism()
                if not still_alive:
                    dead_organisms.append(org_id)
                    caste_name = organism.caste_type.value
                    deaths[caste_name] = deaths.get(caste_name, 0) + 1
                    self.hive_state.population[organism.caste_type] -= 1
                    self.hive_state.total_deaths += 1
                    
                    # Track if a queen died for succession purposes
                    if organism.caste_type == CasteType.QUEEN:
                        queen_died = True
                        print(f"👑💀 QUEEN DEATH: Queen {organism.id} has died at age {organism.age}")
        
        # Remove dead organisms
        for org_id in dead_organisms:
            del self.organisms[org_id]
        
        # If queen died, trigger emergency succession if no other queens exist
        if queen_died:
            living_queens = self._get_organisms_by_caste(CasteType.QUEEN)
            if not living_queens:
                print("🚨 QUEENLESS HIVE: Immediate succession required!")
        
        return deaths
    
    def _random_threat_event(self):
        """Randomly generate threat events"""
        if random.random() < 0.05:  # 5% chance of threat escalation
            current_level = self.hive_state.threat_level.value
            if current_level < 4:  # Don't exceed EXISTENTIAL
                new_level = min(4, current_level + 1)
                self.hive_state.threat_level = ThreatLevel(new_level)
                print(f"🚨 Threat level increased to {self.hive_state.threat_level.name}")
                
        elif random.random() < 0.1:  # 10% chance of threat reduction
            current_level = self.hive_state.threat_level.value
            if current_level > 0:
                new_level = max(0, current_level - 1)
                self.hive_state.threat_level = ThreatLevel(new_level)
                print(f"✅ Threat level reduced to {self.hive_state.threat_level.name}")
    
    def _add_natural_births(self, living_queens_count: int):
        """Add small chance of natural births even without breeding orders"""
        if random.random() < 0.1:  # 10% chance of natural breeding
            breeders = self._get_organisms_by_caste(CasteType.BREEDER)
            if breeders:
                # Natural births tend to be workers (never queens)
                natural_orders = {CasteType.WORKER: 1}
                if random.random() < 0.3:  # 30% chance of other castes
                    caste_options = [CasteType.CLEANER, CasteType.SOLDIER]
                    natural_orders[random.choice(caste_options)] = 1
                
                # Try to breed with available breeders
                for breeder in breeders[:1]:  # Only use first available breeder
                    new_organisms = breeder.spawn_organisms(natural_orders, self.cycle_count, living_queens_count)
                    if new_organisms:
                        for org in new_organisms:
                            self.organisms[self.next_organism_id] = org
                            org.id = self.next_organism_id  # Update ID
                            self.hive_state.population[org.caste_type] += 1
                            self.hive_state.total_births += 1
                            self.next_organism_id += 1
                        print(f"🌱 Natural births: {[f'{org.caste_type.value}-{org.id}' for org in new_organisms]}")
                        break
    
    def _emergency_queen_spawn(self):
        """Emergency queen spawning when hive is queenless"""
        living_queens = self._get_organisms_by_caste(CasteType.QUEEN)
        if not living_queens:
            print("🚨 EMERGENCY QUEEN SPAWN: Creating new queen to save the hive!")
            emergency_queen = Queen(self.next_organism_id, age=random.randint(15, 25))
            emergency_queen.birth_cycle = self.cycle_count
            self.organisms[self.next_organism_id] = emergency_queen
            self.hive_state.population[CasteType.QUEEN] = 1
            self.hive_state.total_births += 1
            self.next_organism_id += 1
            return True
        return False
    
    def simulate_cycle(self):
        """Simulate one complete hive cycle"""
        print(f"\n=== CYCLE {self.cycle_count} ===")
        
        # Age all organisms first
        deaths = self._age_all_organisms()
        if deaths:
            death_report = ", ".join([f"{count} {caste}" for caste, count in deaths.items()])
            print(f"💀 Deaths: {death_report}")
        
        # Count living queens for succession logic
        living_queens = self._get_organisms_by_caste(CasteType.QUEEN)
        living_queens_count = len(living_queens)
        
        # Emergency queen spawn if needed
        if living_queens_count == 0:
            queen_spawned = self._emergency_queen_spawn()
            if queen_spawned:
                living_queens = self._get_organisms_by_caste(CasteType.QUEEN)
                living_queens_count = len(living_queens)
        
        # Check for hive collapse due to no queens (after emergency spawn attempt)
        if living_queens_count == 0:
            print("👑💀 HIVE COLLAPSE: No living queens and emergency spawn failed!")
            return False
        
        # Random threat events
        self._random_threat_event()
        
        # Queen processes stimuli and generates instructions
        all_priorities = {}
        genetic_instructions = {}
        
        for queen in living_queens:
            priorities = queen.process_stimuli(self.hive_state, living_queens_count)
            all_priorities.update(priorities)
            instructions = queen.generate_genetic_instructions(priorities)
            genetic_instructions.update(instructions)
        
        # Handle existential threats - spawn Cerebral Caste
        if self.hive_state.threat_level == ThreatLevel.EXISTENTIAL:
            cerebrals = self._get_organisms_by_caste(CasteType.CEREBRAL)
            if not cerebrals:
                print("🧠 EMERGENCY: Spawning Cerebral Caste for existential threat!")
                cerebral = CerebralCaste(self.next_organism_id)
                cerebral.birth_cycle = self.cycle_count
                self.organisms[self.next_organism_id] = cerebral
                self.hive_state.population[CasteType.CEREBRAL] = 1
                self.hive_state.total_births += 1
                self.next_organism_id += 1
            
            # Cerebral analysis
            for cerebral in self._get_organisms_by_caste(CasteType.CEREBRAL):
                strategies = cerebral.analyze_existential_threat(self.hive_state)
                if 'emergency_spawn' in strategies:
                    genetic_instructions.update(strategies['emergency_spawn'])
                print(f"🧠 Cerebral strategies: {strategies}")
        
        # Workers execute tasks
        workers = self._get_organisms_by_caste(CasteType.WORKER)
        total_food_gathered = 0
        total_waste_generated = 0
        
        for worker in workers:
            if worker.active:
                results = worker.execute_tasks(self.hive_state)
                total_food_gathered += results.get('food_gathered', 0)
                total_waste_generated += results.get('waste_generated', 0)
                
                if 'threat_detected' in results:
                    detected_threat = results['threat_detected']
                    if detected_threat.value > self.hive_state.threat_level.value:
                        self.hive_state.threat_level = detected_threat
                        print(f"⚠️ Worker detected new threat: {detected_threat.name}")
        
        # Update hive state
        self.hive_state.food_level += total_food_gathered
        self.hive_state.waste_level += total_waste_generated
        
        # Soldiers defend against threats
        soldiers = self._get_organisms_by_caste(CasteType.SOLDIER)
        total_defense = 0
        for soldier in soldiers:
            if soldier.active:
                defense = soldier.defend_hive(self.hive_state.threat_level)
                total_defense += defense
        
        if total_defense > 0:
            # Reduce threat based on defense power
            threat_reduction = min(self.hive_state.threat_level.value, total_defense // 20)
            if threat_reduction > 0:
                new_threat_level = max(0, self.hive_state.threat_level.value - threat_reduction)
                self.hive_state.threat_level = ThreatLevel(new_threat_level)
                print(f"🛡️ Soldiers reduced threat to {self.hive_state.threat_level.name}")
        
        # Cleaners process waste
        cleaners = self._get_organisms_by_caste(CasteType.CLEANER)
        total_waste_processed = 0
        total_biomass_recycled = 0
        
        for cleaner in cleaners:
            if cleaner.active:
                results = cleaner.process_waste(self.hive_state.waste_level)
                total_waste_processed += results['waste_processed']
                total_biomass_recycled += results['biomass_recycled']
        
        self.hive_state.waste_level = max(0, self.hive_state.waste_level - total_waste_processed)
        self.hive_state.food_level += total_biomass_recycled
        
        # Bio-Architects maintain structure
        bio_architects = self._get_organisms_by_caste(CasteType.BIO_ARCHITECT)
        for architect in bio_architects:
            if architect.active:
                self.hive_state.structural_integrity = architect.maintain_structure(
                    self.hive_state.structural_integrity
                )
        
        # Breeders spawn new organisms
        births_this_cycle = []
        if genetic_instructions:
            breeders = self._get_organisms_by_caste(CasteType.BREEDER)
            for breeder in breeders:
                if breeder.active:
                    new_organisms = breeder.spawn_organisms(genetic_instructions, self.cycle_count, living_queens_count)
                    for org in new_organisms:
                        org.id = self.next_organism_id  # Assign proper ID
                        self.organisms[self.next_organism_id] = org
                        self.hive_state.population[org.caste_type] += 1
                        self.hive_state.total_births += 1
                        births_this_cycle.append(org)
                        self.next_organism_id += 1
                    
                    if new_organisms:
                        birth_report = ", ".join([f"{org.caste_type.value}-{org.id}" for org in new_organisms])
                        print(f"🐣 Queen-ordered births: {birth_report}")
        
        # Add chance for natural births (but never queens)
        self._add_natural_births(living_queens_count)
        
        # Apply natural consumption and decay
        total_population = sum(self.hive_state.population.values())
        self.hive_state.food_level = max(0, self.hive_state.food_level - total_population // 2)
        self.hive_state.structural_integrity = max(0, self.hive_state.structural_integrity - random.randint(1, 3))
        
        # Print current state
        self.print_status()
        self.cycle_count += 1
        return True
    
    def print_status(self):
        """Print current hive status"""
        total_population = sum(self.hive_state.population.values())
        living_queens = self._get_organisms_by_caste(CasteType.QUEEN)
        queen_info = f" (Queen: {living_queens[0].id}, age {living_queens[0].age})" if living_queens else " (NO QUEEN!)"
        
        print(f"Food: {self.hive_state.food_level} | "
              f"Waste: {self.hive_state.waste_level} | "
              f"Structure: {self.hive_state.structural_integrity}% | "
              f"Threat: {self.hive_state.threat_level.name}")
        
        print(f"Population ({total_population} total){queen_info}:", end=" ")
        for caste_type, count in self.hive_state.population.items():
            if count > 0:
                                print(f"{caste_type.value}: {count}", end=" | ")
        print()
        
        print(f"Total Births: {self.hive_state.total_births} | Total Deaths: {self.hive_state.total_deaths}")
        
    def run_simulation(self, max_cycles: int = 100):
        """Run the simulation for a specified number of cycles"""
        self.running = True
        print("=== HIVE SIMULATION STARTED ===")
        
        for _ in range(max_cycles):
            if not self.simulate_cycle():
                print("=== HIVE COLLAPSED ===")
                break
            time.sleep(0.5)  # Small delay between cycles
            
        self.running = False
        print("=== SIMULATION ENDED ===")
        
    def get_statistics(self) -> Dict[str, any]:
        """Get simulation statistics"""
        return {
            'total_cycles': self.cycle_count,
            'total_population': sum(self.hive_state.population.values()),
            'total_births': self.hive_state.total_births,
            'total_deaths': self.hive_state.total_deaths,
            'current_food': self.hive_state.food_level,
            'current_waste': self.hive_state.waste_level,
            'current_threat': self.hive_state.threat_level.name,
            'current_structure': self.hive_state.structural_integrity,
            'population_by_caste': {caste.value: count for caste, count in self.hive_state.population.items()}
        }

if __name__ == "__main__":
    # Example usage
    simulation = HiveSimulation()
    
    # Run simulation in a separate thread so we can add interactive controls
    def run_sim():
        simulation.run_simulation(max_cycles=100)
    
    sim_thread = threading.Thread(target=run_sim)
    sim_thread.start()
    
    # Simple interactive controls
    try:
        while sim_thread.is_alive():
            cmd = input("\nEnter command (s: stats, q: quit): ").strip().lower()
            if cmd == 's':
                stats = simulation.get_statistics()
                print("\nCurrent Statistics:")
                for key, value in stats.items():
                    if isinstance(value, dict):
                        print(f"{key}:")
                        for k, v in value.items():
                            print(f"  {k}: {v}")
                    else:
                        print(f"{key}: {value}")
            elif cmd == 'q':
                print("Stopping simulation...")
                simulation.running = False
                break
    except KeyboardInterrupt:
        print("\nStopping simulation...")
        simulation.running = False
    
    sim_thread.join()
    print("Simulation ended.")