from .main_window import HiveSimulationApp
from .controls import ControlPanel
from .stats_panel import StatsPanel
from .visualization import HiveVisualization

# Explicit exports for when someone does 'from gui import *'
__all__ = [
    'HiveSimulationApp',
    'ControlPanel',
    'StatsPanel',
    'HiveVisualization'
]

# GUI constants
DEFAULT_WINDOW_SIZE = "800x600"
REFRESH_RATE_MS = 1000  # Default refresh rate in milliseconds

# Common GUI utilities
def center_window(window):
    """Center a tkinter window on screen"""
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')