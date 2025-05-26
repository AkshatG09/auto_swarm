import tkinter as tk
from tkinter import ttk

class StatsPanel(ttk.LabelFrame):
    def __init__(self, parent, simulation):
        super().__init__(parent, text="Hive Statistics", padding=10)
        self.simulation = simulation
        self.stats_vars = {}
        self.setup_stats_display()
        
    def setup_stats_display(self):
        # Cycle counter
        self.add_stat_row("Cycle", "0")
        
        # Resource stats
        self.add_stat_row("Food", "0")
        self.add_stat_row("Waste", "0")
        self.add_stat_row("Structure", "0%")
        self.add_stat_row("Threat Level", "None")
        
        # Population stats
        self.add_stat_row("Total Population", "0")
        self.add_stat_row("Queens", "0")
        self.add_stat_row("Workers", "0")
        self.add_stat_row("Soldiers", "0")
        self.add_stat_row("Cleaners", "0")
        self.add_stat_row("Breeders", "0")
        self.add_stat_row("Bio-Architects", "0")
        self.add_stat_row("Cerebrals", "0")
        
        # Birth/Death stats
        self.add_stat_row("Total Births", "0")
        self.add_stat_row("Total Deaths", "0")
    
    def add_stat_row(self, label, initial_value=""):
        frame = ttk.Frame(self)
        frame.pack(fill=tk.X, pady=2)
        
        lbl = ttk.Label(frame, text=label, width=15, anchor=tk.W)
        lbl.pack(side=tk.LEFT)
        
        var = tk.StringVar(value=initial_value)
        value_lbl = ttk.Label(frame, textvariable=var, width=10, anchor=tk.E)
        value_lbl.pack(side=tk.RIGHT)
        
        self.stats_vars[label] = var
    
    def update_stats(self):
        stats = self.simulation.get_statistics()
        
        # Update basic stats
        self.stats_vars["Cycle"].set(stats['total_cycles'])
        self.stats_vars["Food"].set(stats['current_food'])
        self.stats_vars["Waste"].set(stats['current_waste'])
        self.stats_vars["Structure"].set(f"{stats['current_structure']}%")
        self.stats_vars["Threat Level"].set(stats['current_threat'])
        self.stats_vars["Total Population"].set(stats['total_population'])
        self.stats_vars["Total Births"].set(stats['total_births'])
        self.stats_vars["Total Deaths"].set(stats['total_deaths'])
        
        # Update population by caste
        for caste, count in stats['population_by_caste'].items():
            if caste == "Queen":
                self.stats_vars["Queens"].set(count)
            elif caste == "Worker":
                self.stats_vars["Workers"].set(count)
            elif caste == "Soldier":
                self.stats_vars["Soldiers"].set(count)
            elif caste == "Cleaner":
                self.stats_vars["Cleaners"].set(count)
            elif caste == "Breeder":
                self.stats_vars["Breeders"].set(count)
            elif caste == "Bio-Architect":
                self.stats_vars["Bio-Architects"].set(count)
            elif caste == "Cerebral":
                self.stats_vars["Cerebrals"].set(count)