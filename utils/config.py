"""
Configuration Module
Application constants and settings.
"""

# Application information
APP_NAME = "CAN Data Viewer"
APP_VERSION = "1.1.0"

# Graph settings
MAX_SIGNALS = 5
DEFAULT_GRAPH_HEIGHT = 150
GRAPH_COLORS = [
    '#1f77b4',  # Blue
    '#ff7f0e',  # Orange
    '#2ca02c',  # Green
    '#d62728',  # Red
    '#9467bd',  # Purple
]

# Export settings
EXPORT_FORMATS = {
    'PNG': '*.png',
    'JPEG': '*.jpg',
    'SVG': '*.svg'
}

# Workspace settings
WORKSPACE_EXTENSION = '.workspace'
WORKSPACE_FILTER = 'Workspace Files (*.workspace);;All Files (*)'

# File filters
BLF_FILTER = 'BLF Files (*.blf);;All Files (*)'
DBC_FILTER = 'DBC Files (*.dbc);;All Files (*)'

# UI settings
WINDOW_MIN_WIDTH = 1000
WINDOW_MIN_HEIGHT = 700
SIGNAL_PANEL_WIDTH = 300
STATUS_BAR_HEIGHT = 25
