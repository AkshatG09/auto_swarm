import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class HiveVisualization(ttk.LabelFrame):
    def __init__(self, parent, simulation):
        super().__init__(parent, text="Hive Visualization", padding=10)
        self.simulation = simulation
        self.setup_canvas()
        
    def setup_canvas(self):
        self.canvas = tk.Canvas(self, width=600, height=400, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Simple placeholder visualization
        self.canvas.create_text(300, 200, text="Hive Visualization", 
                              font=("Arial", 24), fill="gray")
        
        # We'll add more visualization elements here
        self.caste_icons = {}
        self.load_caste_icons()
    
    def load_caste_icons(self):
        # Placeholder for caste icons
        # In a real implementation, you'd have small images for each caste
        self.caste_icons = {
            "Queen": "👑",
            "Worker": "🐜",
            "Soldier": "🛡️",
            "Cleaner": "🧹",
            "Breeder": "❤️",
            "Bio-Architect": "🏗️",
            "Cerebral": "🧠"
        }
    
    def update_visualization(self):
        self.canvas.delete("organisms")
        
        stats = self.simulation.get_statistics()
        total_pop = stats['total_population']
        
        if total_pop == 0:
            return
        
        # Simple visualization - display caste counts as text
        y_pos = 50
        for caste, count in stats['population_by_caste'].items():
            if count > 0:
                self.canvas.create_text(
                    100, y_pos, 
                    text=f"{self.caste_icons.get(caste, '')} {caste}: {count}",
                    font=("Arial", 12), 
                    anchor=tk.W,
                    tags="organisms"
                )
                y_pos += 30
        
        # Add food/waste indicators
        food_percent = min(100, stats['current_food'] / 2)  # Scale for visualization
        waste_percent = min(100, stats['current_waste'] / 2)
        
        self.canvas.create_rectangle(
            300, 50, 350, 250, 
            outline="black", 
            fill="white",
            tags="organisms"
        )
        self.canvas.create_rectangle(
            300, 250 - food_percent * 2, 350, 250,
            outline="green",
            fill="lightgreen",
            tags="organisms"
        )
        self.canvas.create_text(325, 270, text="Food", tags="organisms")
        
        self.canvas.create_rectangle(
            400, 50, 450, 250, 
            outline="black", 
            fill="white",
            tags="organisms"
        )
        self.canvas.create_rectangle(
            400, 250 - waste_percent * 2, 450, 250,
            outline="brown",
            fill="tan",
            tags="organisms"
        )
        self.canvas.create_text(425, 270, text="Waste", tags="organisms")