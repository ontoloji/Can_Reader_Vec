"""
Graph Panel Widget
Right panel with 5 synchronized graphs for signal visualization.
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSplitter
from PyQt5.QtCore import Qt
import pyqtgraph as pg
import numpy as np
from typing import List, Dict, Tuple, Optional


class GraphPanel(QWidget):
    """Widget containing 5 synchronized graphs."""
    
    def __init__(self, max_graphs: int = 5, colors: List[str] = None):
        super().__init__()
        self.max_graphs = max_graphs
        self.colors = colors if colors else [
            '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'
        ]
        self.plot_widgets: List[Optional[pg.PlotWidget]] = []
        self.plot_items: List[Optional[pg.PlotDataItem]] = []
        self.signal_info: List[Optional[Dict]] = [None] * max_graphs
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create splitter for resizable graphs
        splitter = QSplitter(Qt.Vertical)
        
        # Create plot widgets
        for i in range(self.max_graphs):
            plot_widget = pg.PlotWidget()
            plot_widget.setBackground('w')
            plot_widget.showGrid(x=True, y=True, alpha=0.3)
            plot_widget.setLabel('left', 'Value')
            plot_widget.setLabel('bottom', 'Time', units='s')
            plot_widget.addLegend()
            
            # Enable mouse interaction
            plot_widget.setMouseEnabled(x=True, y=True)
            
            # Link X axis to first plot for synchronization
            if i > 0 and self.plot_widgets:
                plot_widget.setXLink(self.plot_widgets[0])
            
            self.plot_widgets.append(plot_widget)
            self.plot_items.append(None)
            splitter.addWidget(plot_widget)
        
        layout.addWidget(splitter)
        self.setLayout(layout)
    
    def plot_signal(
        self,
        index: int,
        time_data: np.ndarray,
        value_data: np.ndarray,
        signal_info: Dict[str, str]
    ):
        """
        Plot a signal on a specific graph.
        
        Args:
            index: Graph index (0-4)
            time_data: Time values array
            value_data: Signal values array
            signal_info: Dictionary with signal metadata (message, signal, unit)
        """
        if index >= self.max_graphs:
            return
        
        plot_widget = self.plot_widgets[index]
        
        # Clear previous plot
        if self.plot_items[index]:
            plot_widget.removeItem(self.plot_items[index])
        
        # Create new plot
        color = self.colors[index % len(self.colors)]
        pen = pg.mkPen(color=color, width=2)
        
        label = f"{signal_info['message']}.{signal_info['signal']}"
        if signal_info['unit']:
            label += f" ({signal_info['unit']})"
        
        plot_item = plot_widget.plot(
            time_data,
            value_data,
            pen=pen,
            name=label
        )
        
        self.plot_items[index] = plot_item
        self.signal_info[index] = signal_info
        
        # Update axis label
        y_label = signal_info['signal']
        if signal_info['unit']:
            y_label += f" ({signal_info['unit']})"
        plot_widget.setLabel('left', y_label)
    
    def clear_graph(self, index: int):
        """
        Clear a specific graph.
        
        Args:
            index: Graph index (0-4)
        """
        if index >= self.max_graphs:
            return
        
        plot_widget = self.plot_widgets[index]
        
        if self.plot_items[index]:
            plot_widget.removeItem(self.plot_items[index])
            self.plot_items[index] = None
        
        self.signal_info[index] = None
        plot_widget.setLabel('left', 'Value')
    
    def clear_all(self):
        """Clear all graphs."""
        for i in range(self.max_graphs):
            self.clear_graph(i)
    
    def reset_zoom(self):
        """Reset zoom to show all data."""
        for plot_widget in self.plot_widgets:
            plot_widget.autoRange()
    
    def fit_to_data(self):
        """Fit view to data range (alias for reset_zoom)."""
        self.reset_zoom()
    
    def get_view_range(self) -> Dict[str, float]:
        """
        Get the current view range of the first plot.
        
        Returns:
            Dictionary with x_min and x_max
        """
        if self.plot_widgets:
            view_range = self.plot_widgets[0].viewRange()
            return {
                'x_min': view_range[0][0],
                'x_max': view_range[0][1]
            }
        return {'x_min': 0, 'x_max': 100}
    
    def set_view_range(self, x_min: float, x_max: float):
        """
        Set the view range for all plots.
        
        Args:
            x_min: Minimum X value
            x_max: Maximum X value
        """
        for plot_widget in self.plot_widgets:
            plot_widget.setXRange(x_min, x_max, padding=0)
    
    def export_graph(self, index: int, filepath: str) -> bool:
        """
        Export a specific graph to file.
        
        Args:
            index: Graph index (0-4)
            filepath: Path to save the image
            
        Returns:
            True if successful
        """
        if index >= self.max_graphs:
            return False
        
        from utils.export import GraphExporter
        return GraphExporter.export_graph(self.plot_widgets[index], filepath)
    
    def export_all(self, base_filepath: str) -> bool:
        """
        Export all graphs to separate files.
        
        Args:
            base_filepath: Base filepath for exports
            
        Returns:
            True if successful
        """
        from utils.export import GraphExporter
        return GraphExporter.export_all_graphs(self.plot_widgets, base_filepath)
