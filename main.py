import tkinter as tk
from gui.main_window import HiveSimulationApp
from simulation.core import HiveSimulation

def main():
    root = tk.Tk()
    root.title("Hive Simulation")
    
    # Create simulation core
    simulation = HiveSimulation()
    
    # Create GUI app
    app = HiveSimulationApp(root, simulation)
    
    root.mainloop()

if __name__ == "__main__":
    main()