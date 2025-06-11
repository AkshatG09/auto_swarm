import tkinter as tk
from tkinter import ttk

class ControlPanel(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.setup_controls()
        
    def setup_controls(self):
        # Start/Stop buttons
        self.start_button = ttk.Button(self, text="Start", command=self.app.start_simulation)
        self.start_button.grid(row=0, column=0, padx=5, pady=5)
        
        self.stop_button = ttk.Button(self, text="Stop", command=self.app.stop_simulation)
        self.stop_button.grid(row=0, column=1, padx=5, pady=5)
        
        # Step button
        self.step_button = ttk.Button(self, text="Step", command=self.app.step_simulation)
        self.step_button.grid(row=0, column=2, padx=5, pady=5)
        
        # Speed control
        self.speed_label = ttk.Label(self, text="Speed:")
        self.speed_label.grid(row=1, column=0, padx=5, pady=5)
          # Speed scale: 0.5 to 5 cycles per second
        self.speed_scale = ttk.Scale(self, from_=0.5, to=5.0, orient=tk.HORIZONTAL)
        self.speed_scale.set(1.0)  # Default to 1 cycle per second
        self.speed_scale.grid(row=1, column=1, columnspan=2, padx=5, pady=5)