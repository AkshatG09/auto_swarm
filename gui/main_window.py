import tkinter as tk
from tkinter import ttk
from .controls import ControlPanel
from .stats_panel import StatsPanel
from .visualization import HiveVisualization

class HiveSimulationApp:
    def __init__(self, root, simulation):
        self.root = root
        self.simulation = simulation
        self.running = False
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Visualization area
        self.visualization = HiveVisualization(self.main_frame, self.simulation)
        self.visualization.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Control panel
        self.control_panel = ControlPanel(self.main_frame, self)
        self.control_panel.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        
        # Stats panel
        self.stats_panel = StatsPanel(self.main_frame, self.simulation)
        self.stats_panel.grid(row=0, column=1, rowspan=2, padx=5, pady=5, sticky=(tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)
    
    def start_simulation(self):
        if not self.running:
            self.running = True
            self.run_simulation_cycle()
    
    def stop_simulation(self):
        self.running = False
    
    def run_simulation_cycle(self):
        if self.running:
            self.simulation.simulate_cycle()
            self.stats_panel.update_stats()
            self.visualization.update_visualization()
            self.root.after(1000, self.run_simulation_cycle)  # Run every second
    
    def step_simulation(self):
        if not self.running:
            self.simulation.simulate_cycle()
            self.stats_panel.update_stats()
            self.visualization.update_visualization()