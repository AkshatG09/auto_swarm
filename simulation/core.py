import random
import time
from typing import Dict, List
from entities import HiveState, Organism, Queen, Worker, Soldier, Cleaner, Breeder, BioArchitect, CerebralCaste
from constants.enums import CasteType, ThreatLevel
from constants.settings import INITIAL_POPULATION, INITIAL_HIVE_STATE


class HiveSimulation:
    def __init__(self):
        self.hive_state = HiveState()
        self.organisms = {}
        self.cycle_count = 0
        self.running = False
        self.next_organism_id = 1000
        self._initialize_organisms()
        
    def _initialize_organisms(self):
        organism_id = 1
        
        for _ in range(self.hive_state.population[CasteType.QUEEN]):
            self.organisms[organism_id] = Queen(organism_id, age=random.randint(20, 40))
            organism_id += 1

            
        for _ in range(self.hive_state.population[CasteType.WORKER]):
            self.organisms[organism_id] = Worker(organism_id, age=random.randint(0, 15))
            organism_id += 1
            
        for _ in range(self.hive_state.population[CasteType.SOLDIER]):
            self.organisms[organism_id] = Soldier(organism_id, age=random.randint(0, 12))
            organism_id += 1
            
        for _ in range(self.hive_state.population[CasteType.CLEANER]):
            self.organisms[organism_id] = Cleaner(organism_id, age=random.randint(0, 18))
            organism_id += 1
            
        for _ in range(self.hive_state.population[CasteType.BREEDER]):
            self.organisms[organism_id] = Breeder(organism_id, age=random.randint(5, 20))
            organism_id += 1
            
        for _ in range(self.hive_state.population[CasteType.BIO_ARCHITECT]):
            self.organisms[organism_id] = BioArchitect(organism_id, age=random.randint(0, 25))
            organism_id += 1
        
        self.next_organism_id = organism_id
    
    def _get_organisms_by_caste(self, caste_type: CasteType) -> List[Organism]:
        return [org for org in self.organisms.values() 
                if org.caste_type == caste_type and org.active]
    
    def _age_all_organisms(self) -> Dict[str, int]:
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
                    
                    if organism.caste_type == CasteType.QUEEN:
                        queen_died = True
                        print(f"👑💀 QUEEN DEATH: Queen {organism.id} has died at age {organism.age}")
        
        for org_id in dead_organisms:
            del self.organisms[org_id]
        
        if queen_died:
            living_queens = self._get_organisms_by_caste(CasteType.QUEEN)
            if not living_queens:
                print("🚨 QUEENLESS HIVE: Immediate succession required!")
        
        return deaths
    
    def _random_threat_event(self):
        if random.random() < 0.05:
            current_level = self.hive_state.threat_level.value
            if current_level < 4:
                new_level = min(4, current_level + 1)
                self.hive_state.threat_level = ThreatLevel(new_level)
                print(f"🚨 Threat level increased to {self.hive_state.threat_level.name}")
                
        elif random.random() < 0.1:
            current_level = self.hive_state.threat_level.value
            if current_level > 0:
                new_level = max(0, current_level - 1)
                self.hive_state.threat_level = ThreatLevel(new_level)
                print(f"✅ Threat level reduced to {self.hive_state.threat_level.name}")
    
    def _add_natural_births(self, living_queens_count: int):
        if random.random() < 0.1:
            breeders = self._get_organisms_by_caste(CasteType.BREEDER)
            if breeders:
                natural_orders = {CasteType.WORKER: 1}
                if random.random() < 0.3:
                    caste_options = [CasteType.CLEANER, CasteType.SOLDIER]
                    natural_orders[random.choice(caste_options)] = 1
                
                for breeder in breeders[:1]:
                    new_organisms = breeder.spawn_organisms(natural_orders, self.cycle_count, living_queens_count)
                    if new_organisms:
                        for org in new_organisms:
                            self.organisms[self.next_organism_id] = org
                            org.id = self.next_organism_id
                            self.hive_state.population[org.caste_type] += 1
                            self.hive_state.total_births += 1
                            self.next_organism_id += 1
                        print(f"🌱 Natural births: {[f'{org.caste_type.value}-{org.id}' for org in new_organisms]}")
                        break
    
    def _emergency_queen_spawn(self):
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
        print(f"\n=== CYCLE {self.cycle_count} ===")
          # Check for collapse conditions with grace periods and chances for recovery
        if self.hive_state.structural_integrity <= 0:
            if not hasattr(self, '_structure_critical_cycles'):
                self._structure_critical_cycles = 0
            self._structure_critical_cycles += 1
            
            # Give 3 cycles for bio-architects to potentially fix it
            if self._structure_critical_cycles >= 3:
                print("🏗️💥 CATASTROPHIC COLLAPSE: Hive structure has completely failed (0% integrity)")
                print("The entire colony has been crushed under the collapsing structure.")
                return False
            else:
                print(f"⚠️ IMMINENT COLLAPSE: Structure at 0% - {3 - self._structure_critical_cycles} cycles until collapse!")
        else:
            self._structure_critical_cycles = 0
            
        if self.hive_state.waste_level >= 200:
            if not hasattr(self, '_waste_critical_cycles'):
                self._waste_critical_cycles = 0
            self._waste_critical_cycles += 1
            
            # Give 5 cycles for cleaners to potentially fix it
            if self._waste_critical_cycles >= 5:
                print("☠️ TOXIC OVERLOAD: Waste levels have reached critical mass (200+)")
                print("The colony has been overwhelmed by toxic waste buildup.")
                return False
            else:
                print(f"⚠️ CRITICAL WASTE: Levels at {self.hive_state.waste_level} - {5 - self._waste_critical_cycles} cycles until toxic collapse!")
          # Check for vulnerable colony condition (no breeders and no soldiers during threat)
        breeders = self._get_organisms_by_caste(CasteType.BREEDER)
        soldiers = self._get_organisms_by_caste(CasteType.SOLDIER)
        
        if len(breeders) == 0 and len(soldiers) == 0 and self.hive_state.threat_level != ThreatLevel.NONE:
            if not hasattr(self, '_vulnerable_cycles'):
                self._vulnerable_cycles = 0
            self._vulnerable_cycles += 1
            
            # Calculate death chance based on threat level and time without defense
            # Base rates: LOW: 5%, MEDIUM: 10%, HIGH: 15%, EXISTENTIAL: 20%
            base_death_chance = 0.05 * self.hive_state.threat_level.value
            
            # Increase chance based on how long the colony has been vulnerable
            death_chance = min(0.75, base_death_chance + (self._vulnerable_cycles * 0.02))
            
            # Kill organisms based on threat level
            dead_organisms = []
            for org_id, organism in self.organisms.items():
                if organism.active and random.random() < death_chance:
                    # Queens and workers have a slightly better chance of survival
                    if organism.caste_type in [CasteType.QUEEN, CasteType.WORKER]:
                        if random.random() > 0.3:  # 70% chance to survive this round
                            continue
                    organism.active = False
                    dead_organisms.append(org_id)
            
            if dead_organisms:
                print(f"⚠️ DEFENSE CRISIS: No breeders or soldiers during threat level {self.hive_state.threat_level.name}")
                print(f"⏳ Cycles without defense: {self._vulnerable_cycles} (Death chance: {death_chance:.1%})")
                
                for org_id in dead_organisms:
                    org_type = self.organisms[org_id].caste_type
                    self.hive_state.population[org_type] -= 1
                    self.hive_state.total_deaths += 1
                    print(f"💀 {org_type.value}-{org_id} has perished due to undefended threat")
                    del self.organisms[org_id]
            
            # If all organisms are dead, colony collapses
            if sum(self.hive_state.population.values()) == 0:
                print("💀 COLONY EXTINCTION: All organisms have perished due to undefended threats")
                return False
        else:
            # Reset vulnerable cycles if we have either breeders or soldiers
            self._vulnerable_cycles = 0
        
        # If there are no breeders and there's a threat, colony dies based on threat level
        breeders = self._get_organisms_by_caste(CasteType.BREEDER)
        if len(breeders) == 0 and self.hive_state.threat_level != ThreatLevel.NONE:
            threat_multiplier = self.hive_state.threat_level.value
            death_chance = 0.2 * threat_multiplier  # 20% chance per threat level
            
            # Kill organisms based on threat level
            dead_organisms = []
            for org_id, organism in self.organisms.items():
                if organism.active and random.random() < death_chance:
                    organism.active = False
                    dead_organisms.append(org_id)
                    self.hive_state.population[organism.caste_type] -= 1
                    self.hive_state.total_deaths += 1
                    
            if dead_organisms:
                print(f"⚠️ BREEDER EXTINCTION EVENT: No breeders to maintain the population during threat level {self.hive_state.threat_level.name}")
                print(f"💀 {len(dead_organisms)} organisms died in this cycle due to the crisis")
                
                for org_id in dead_organisms:
                    del self.organisms[org_id]
                
                # If all organisms are dead, colony collapses
                if sum(self.hive_state.population.values()) == 0:
                    print("💀 COLONY EXTINCTION: All organisms have perished due to the breeder crisis")
                    return False
        
        deaths = self._age_all_organisms()
        if deaths:
            death_report = ", ".join([f"{count} {caste}" for caste, count in deaths.items()])
            print(f"💀 Deaths: {death_report}")
        
        living_queens = self._get_organisms_by_caste(CasteType.QUEEN)
        living_queens_count = len(living_queens)
        
        if living_queens_count == 0:
            queen_spawned = self._emergency_queen_spawn()
            if queen_spawned:
                living_queens = self._get_organisms_by_caste(CasteType.QUEEN)
                living_queens_count = len(living_queens)
        
        if living_queens_count == 0:
            print("👑💀 HIVE COLLAPSE: No living queens and emergency spawn failed!")
            return False
        
        self._random_threat_event()
        
        all_priorities = {}
        genetic_instructions = {}
        
        for queen in living_queens:
            priorities = queen.process_stimuli(self.hive_state, living_queens_count)
            all_priorities.update(priorities)
            instructions = queen.generate_genetic_instructions(priorities)
            genetic_instructions.update(instructions)
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
        
        self.hive_state.food_level += total_food_gathered
        self.hive_state.waste_level += total_waste_generated
        
        soldiers = self._get_organisms_by_caste(CasteType.SOLDIER)
        total_defense = 0
        for soldier in soldiers:
            if soldier.active:
                defense = soldier.defend_hive(self.hive_state.threat_level)
                total_defense += defense
        
        if total_defense > 0:
            threat_reduction = min(self.hive_state.threat_level.value, total_defense // 20)
            if threat_reduction > 0:
                new_threat_level = max(0, self.hive_state.threat_level.value - threat_reduction)
                self.hive_state.threat_level = ThreatLevel(new_threat_level)
                print(f"🛡️ Soldiers reduced threat to {self.hive_state.threat_level.name}")
        
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
        
        bio_architects = self._get_organisms_by_caste(CasteType.BIO_ARCHITECT)
        for architect in bio_architects:
            if architect.active:
                self.hive_state.structural_integrity = architect.maintain_structure(
                    self.hive_state.structural_integrity
                )
        
        births_this_cycle = []
        if genetic_instructions:
            breeders = self._get_organisms_by_caste(CasteType.BREEDER)
            for breeder in breeders:
                if breeder.active:
                    new_organisms = breeder.spawn_organisms(genetic_instructions, self.cycle_count, living_queens_count)
                    for org in new_organisms:
                        org.id = self.next_organism_id
                        self.organisms[self.next_organism_id] = org
                        self.hive_state.population[org.caste_type] += 1
                        self.hive_state.total_births += 1
                        births_this_cycle.append(org)
                        self.next_organism_id += 1
                    
                    if new_organisms:
                        birth_report = ", ".join([f"{org.caste_type.value}-{org.id}" for org in new_organisms])
                        print(f"🐣 Queen-ordered births: {birth_report}")

        # Emergency worker replenishment system
        if (self.hive_state.population[CasteType.WORKER] < 3 and 
            self.cycle_count > 10):  # Don't trigger in early game
            # Override breeding orders if necessary
            if not any('emergency' in p for p in all_priorities):
                print("⚡ AUTO-EMERGENCY: Force-spawning workers")
                genetic_instructions[CasteType.WORKER] = max(
                    genetic_instructions.get(CasteType.WORKER, 0),
                    3  # Minimum 3 workers
                )
        
        # Prevent total worker extinction
        if self.hive_state.population[CasteType.WORKER] == 0:
            print("💥 CRITICAL FAILURE: No workers left - spawning emergency batch")
            emergency_worker = Worker(self.next_organism_id, age=0)
            emergency_worker.birth_cycle = self.cycle_count
            self.organisms[self.next_organism_id] = emergency_worker
            self.hive_state.population[CasteType.WORKER] += 1
            self.hive_state.total_births += 1
            self.next_organism_id += 1
        
        self._add_natural_births(living_queens_count)
        
        total_population = sum(self.hive_state.population.values())
        self.hive_state.food_level = max(0, self.hive_state.food_level - total_population // 2)
        self.hive_state.structural_integrity = max(0, self.hive_state.structural_integrity - random.randint(1, 3))
        
        self.print_status()
        self.cycle_count += 1
        return True

    def print_status(self):
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
        self.running = True
        print("=== HIVE SIMULATION STARTED ===")
        
        for _ in range(max_cycles):
            if not self.simulate_cycle():
                print("=== HIVE COLLAPSED ===")
                break
            time.sleep(0.5)
            
        self.running = False
        print("=== SIMULATION ENDED ===")
        
    def get_statistics(self) -> Dict[str, any]:
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