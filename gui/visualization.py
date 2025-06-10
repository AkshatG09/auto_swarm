import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class HiveVisualization(ttk.LabelFrame):
    def __init__(self, parent, simulation):
        super().__init__(parent, text="Hive Visualization", padding=10)
        self.simulation = simulation
        self.setup_canvas()
        
    def setup_canvas(self):
        self.canvas = tk.Canvas(self, width=800, height=400, bg="#f0f0f0")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Load caste icons and colors
        self.caste_icons = {
            "Queen": "👑",
            "Worker": "🐜",
            "Soldier": "🛡️",
            "Cleaner": "🧹",
            "Breeder": "❤️",
            "Bio-Architect": "🏗️",
            "Cerebral": "🧠"
        }
        
        self.status_colors = {
            "healthy": "#4CAF50",      # Green
            "warning": "#FFC107",      # Yellow
            "danger": "#F44336",       # Red
            "critical": "#B71C1C",     # Dark Red
            "neutral": "#2196F3"       # Blue
        }
        
    def draw_resource_gauge(self, x, y, width, height, value, max_value, title, color):
        # Draw gauge background
        self.canvas.create_rectangle(x, y, x + width, y + height, 
                                   fill="white", outline="#999999")
        
        # Calculate fill height
        fill_height = (height * min(value, max_value)) / max_value
        
        # Draw gauge fill
        if fill_height > 0:
            self.canvas.create_rectangle(x, y + height - fill_height, 
                                       x + width, y + height,
                                       fill=color, outline=color)
        
        # Draw title and value
        self.canvas.create_text(x + width/2, y - 20, 
                              text=f"{title}: {value}", 
                              anchor=tk.CENTER,
                              font=("Arial", 10, "bold"))
    
    def draw_population_chart(self, x, y, stats):
        spacing = 100
        bar_width = 40
        scale_factor = 2  # Height multiplier for bars
        
        for i, (caste, count) in enumerate(stats['population_by_caste'].items()):
            if count > 0:
                # Draw bar
                bar_height = count * scale_factor
                bar_x = x + (i * spacing)
                bar_y = y - bar_height
                
                # Color based on caste health
                color = self.get_caste_health_color(caste, stats)
                
                self.canvas.create_rectangle(bar_x, bar_y,
                                          bar_x + bar_width, y,
                                          fill=color, outline="#666666")
                
                # Draw icon and count
                self.canvas.create_text(bar_x + bar_width/2, y + 20,
                                      text=f"{self.caste_icons.get(caste, '?')}\n{count}",
                                      anchor=tk.N, justify=tk.CENTER)
    
    def get_caste_health_color(self, caste, stats):
        if caste == "Queen" and stats['population_by_caste'].get("Queen", 0) < 1:
            return self.status_colors["critical"]
        elif caste == "Soldier" and stats['current_threat'] != "NONE":
            return self.status_colors["danger"] if stats['population_by_caste'].get("Soldier", 0) < 3 else self.status_colors["healthy"]
        elif caste == "Worker" and stats['population_by_caste'].get("Worker", 0) < 3:
            return self.status_colors["danger"]
        elif caste == "Breeder" and stats['population_by_caste'].get("Breeder", 0) < 1:
            return self.status_colors["warning"]
        return self.status_colors["neutral"]
    
    def draw_threat_indicator(self, x, y, threat_level):
        threat_colors = {
            "NONE": "#4CAF50",
            "LOW": "#FFC107",
            "MEDIUM": "#FF9800",
            "HIGH": "#F44336",
            "EXISTENTIAL": "#B71C1C"
        }
        
        radius = 30
        color = threat_colors.get(threat_level, "#999999")
        
        # Draw threat indicator circle
        self.canvas.create_oval(x - radius, y - radius,
                              x + radius, y + radius,
                              fill=color, outline="#666666")
        
        # Draw threat level text
        self.canvas.create_text(x, y, text=threat_level,
                              font=("Arial", 10, "bold"),
                              fill="white")
        
        self.canvas.create_text(x, y - radius - 15,
                              text="Threat Level",
                              font=("Arial", 10))
    
    def update_visualization(self):
        self.canvas.delete("all")
        stats = self.simulation.get_statistics()
        
        # Draw resource gauges
        self.draw_resource_gauge(50, 100, 40, 200, stats['current_food'], 200, "Food", self.status_colors["neutral"])
        self.draw_resource_gauge(120, 100, 40, 200, stats['current_waste'], 200, "Waste", 
                               self.status_colors["danger"] if stats['current_waste'] >= 150 else self.status_colors["warning"])
        self.draw_resource_gauge(190, 100, 40, 200, stats['current_structure'], 100, "Structure",
                               self.status_colors["critical"] if stats['current_structure'] <= 30 else 
                               self.status_colors["warning"] if stats['current_structure'] <= 70 else 
                               self.status_colors["healthy"])
        
        # Draw population chart
        self.draw_population_chart(300, 300, stats)
        
        # Draw threat indicator
        self.draw_threat_indicator(150, 50, stats['current_threat'])
        
        # Draw total population and cycles
        self.canvas.create_text(400, 30, 
                              text=f"Total Population: {stats['total_population']} | Cycle: {stats['total_cycles']}",
                              font=("Arial", 12, "bold"))
        
        # Draw birth/death statistics
        self.canvas.create_text(400, 50,
                              text=f"Births: {stats['total_births']} | Deaths: {stats['total_deaths']}",
                              font=("Arial", 10))