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
        self.setup_styles()
        self.setup_ui()
        
    def setup_styles(self):
        # Configure styles for different stat types
        style = ttk.Style()
        
        # Resource-related styles
        style.configure("food.TLabel", foreground="green")
        style.configure("waste.TLabel", foreground="brown")
        style.configure("structure.TLabel", foreground="blue")
        style.configure("threat.TLabel", foreground="red")
        
        # Population-related styles
        style.configure("queen.TLabel", foreground="purple")
        style.configure("worker.TLabel", foreground="brown")
        style.configure("soldier.TLabel", foreground="red")
        style.configure("cleaner.TLabel", foreground="green")
        style.configure("breeder.TLabel", foreground="pink")
        style.configure("architect.TLabel", foreground="blue")
        style.configure("cerebral.TLabel", foreground="purple")
        
        # General styling
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabelframe", background="#f0f0f0")
        style.configure("TLabelframe.Label", font=("Arial", 10, "bold"))
        
    def setup_ui(self):
        # Configure the root window
        self.root.title("Auto-Swarm Colony Simulator")
        self.root.configure(bg="#f0f0f0")
        self.root.minsize(1200, 800)
        
        # Main container
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Left panel - Visualization and Controls
        left_panel = ttk.Frame(self.main_frame)
        left_panel.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Visualization area with border
        viz_frame = ttk.LabelFrame(left_panel, text="Colony Visualization", padding=5)
        viz_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.visualization = HiveVisualization(viz_frame, self.simulation)
        self.visualization.pack(fill=tk.BOTH, expand=True)
        
        # Control panel
        self.control_panel = ControlPanel(left_panel, self)
        self.control_panel.pack(fill=tk.X, padx=5, pady=5)
        
        # Right panel - Statistics
        self.stats_panel = StatsPanel(self.main_frame, self.simulation)
        self.stats_panel.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=3)  # Visualization takes more space
        self.main_frame.columnconfigure(1, weight=1)  # Stats panel takes less space
        self.main_frame.rowconfigure(0, weight=1)
    
    def start_simulation(self):
        if not self.running:
            self.running = True
            self.run_simulation_cycle()
    
    def stop_simulation(self):
        self.running = False
    
    def run_simulation_cycle(self):
        if self.running:
            try:
                cycle_success = self.simulation.simulate_cycle()
                if not cycle_success:
                    self.stop_simulation()
                    
                self.stats_panel.update_stats()
                self.visualization.update_visualization()
                
                # Dynamic cycle speed based on control panel setting
                cycle_speed = int(1000 / self.control_panel.speed_scale.get())
                self.root.after(cycle_speed, self.run_simulation_cycle)
            except Exception as e:
                print(f"Simulation error: {e}")
                self.stop_simulation()
    
    def step_simulation(self):
        if not self.running:
            try:
                self.simulation.simulate_cycle()
                self.stats_panel.update_stats()
                self.visualization.update_visualization()
            except Exception as e:
                print(f"Simulation error: {e}")