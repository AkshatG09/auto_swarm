import tkinter as tk
from tkinter import ttk

class StatsPanel(ttk.LabelFrame):
    def __init__(self, parent, simulation):
        super().__init__(parent, text="Colony Statistics", padding=10)
        self.simulation = simulation
        self.stats_vars = {}
        self.setup_stats_display()
        
    def setup_stats_display(self):
        # Create sections
        resources_frame = self.create_section("Resources")
        population_frame = self.create_section("Population")
        history_frame = self.create_section("History")
        status_frame = self.create_section("Colony Status")
        
        # Resource stats in resources_frame
        self.add_stat_row(resources_frame, "Food Level", "0", "food")
        self.add_stat_row(resources_frame, "Waste Level", "0", "waste")
        self.add_stat_row(resources_frame, "Structure", "0%", "structure")
        self.add_stat_row(resources_frame, "Threat Level", "None", "threat")
        
        # Population stats in population_frame 
        self.add_stat_row(population_frame, "Total Population", "0")
        self.add_stat_row(population_frame, "Queens", "0", "queen")
        self.add_stat_row(population_frame, "Workers", "0", "worker")
        self.add_stat_row(population_frame, "Soldiers", "0", "soldier")
        self.add_stat_row(population_frame, "Cleaners", "0", "cleaner")
        self.add_stat_row(population_frame, "Breeders", "0", "breeder")
        self.add_stat_row(population_frame, "Bio-Architects", "0", "architect")
        
        # History in history_frame
        self.add_stat_row(history_frame, "Current Cycle", "0")
        self.add_stat_row(history_frame, "Total Births", "0")
        self.add_stat_row(history_frame, "Total Deaths", "0")
        
        # Status indicators in status_frame
        self.status_label = ttk.Label(status_frame, text="Colony Status: Healthy", font=("Arial", 10, "bold"))
        self.status_label.pack(pady=5)
        
        self.warnings_text = tk.Text(status_frame, height=4, width=30, wrap=tk.WORD, 
                                   font=("Arial", 9))
        self.warnings_text.pack(pady=5)
        
    def create_section(self, title):
        frame = ttk.LabelFrame(self, text=title, padding=5)
        frame.pack(fill=tk.X, padx=5, pady=5)
        return frame
    
    def add_stat_row(self, parent, label, initial_value="", stat_type=None):
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=2)
        
        lbl = ttk.Label(frame, text=label, width=15, anchor=tk.W)
        lbl.pack(side=tk.LEFT)
        
        var = tk.StringVar(value=initial_value)
        if stat_type:
            value_lbl = ttk.Label(frame, textvariable=var, width=10, anchor=tk.E)
            value_lbl.configure(style=f"{stat_type}.TLabel")
        else:
            value_lbl = ttk.Label(frame, textvariable=var, width=10, anchor=tk.E)
        value_lbl.pack(side=tk.RIGHT)
        
        self.stats_vars[label] = var
    
    def update_stats(self):
        stats = self.simulation.get_statistics()
        
        # Update basic stats
        self.stats_vars["Current Cycle"].set(stats['total_cycles'])
        self.stats_vars["Food Level"].set(stats['current_food'])
        self.stats_vars["Waste Level"].set(stats['current_waste'])
        self.stats_vars["Structure"].set(f"{stats['current_structure']}%")
        self.stats_vars["Threat Level"].set(stats['current_threat'])
        self.stats_vars["Total Population"].set(stats['total_population'])
        self.stats_vars["Total Births"].set(stats['total_births'])
        self.stats_vars["Total Deaths"].set(stats['total_deaths'])
        
        # Update population by caste
        for caste, count in stats['population_by_caste'].items():
            if caste in self.stats_vars:
                self.stats_vars[caste].set(count)
        
        # Update status and warnings
        self.update_status_and_warnings(stats)
    
    def update_status_and_warnings(self, stats):
        warnings = []
        status = "Healthy"
        
        # Check critical conditions
        if stats['current_structure'] <= 30:
            warnings.append("⚠️ Critical structural damage!")
            status = "Critical"
        elif stats['current_structure'] <= 70:
            warnings.append("⚡ Structure needs maintenance")
            
        if stats['current_waste'] >= 150:
            warnings.append("☠️ Dangerous waste levels!")
            status = "Critical"
        elif stats['current_waste'] >= 100:
            warnings.append("⚡ High waste accumulation")
            
        if stats['population_by_caste'].get("Queen", 0) < 1:
            warnings.append("👑 No living queen!")
            status = "Critical"
            
        if stats['current_threat'] != "NONE":
            threat_warning = f"🚨 Active {stats['current_threat'].lower()} threat"
            if stats['population_by_caste'].get("Soldier", 0) < 3:
                threat_warning += " - Low defense!"
            warnings.append(threat_warning)
            
        if stats['population_by_caste'].get("Worker", 0) < 3:
            warnings.append("⚡ Critical worker shortage")
            
        if stats['population_by_caste'].get("Breeder", 0) < 1:
            warnings.append("❗ No breeders available")
        
        # Update status label with appropriate color
        if status == "Critical":
            self.status_label.configure(text="Colony Status: CRITICAL", foreground="red")
        elif warnings:
            self.status_label.configure(text="Colony Status: WARNING", foreground="orange")
        else:
            self.status_label.configure(text="Colony Status: Healthy", foreground="green")
        
        # Update warnings text
        self.warnings_text.delete(1.0, tk.END)
        if warnings:
            self.warnings_text.insert(tk.END, "\n".join(warnings))
        else:
            self.warnings_text.insert(tk.END, "No active warnings")