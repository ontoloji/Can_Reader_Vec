"""
Graph Panel Widget
Right panel with dynamic number of synchronized graphs for signal visualization.
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSplitter
from PyQt5.QtCore import Qt
import pyqtgraph as pg
import numpy as np
from typing import List, Dict, Tuple, Optional


class GraphPanel(QWidget):
    """Widget containing dynamically adjustable number of synchronized graphs."""
    
    def __init__(self, max_graphs: int = 5, colors: List[str] = None):
        super().__init__()
        self.max_graphs = max_graphs
        self.colors = colors if colors else [
            '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
            '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
        ]
        self.current_graph_count = 1  # Default to 1 graph
        self.plot_widgets: List[Optional[pg.PlotWidget]] = []
        self.plot_items: List[Optional[pg.PlotDataItem]] = []
        self.signal_info: List[Optional[Dict]] = []
        self.signal_data: List[Optional[Dict]] = []  # Store signal data for re-plotting
        self.splitter = None
        self.is_dark_mode = False
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        # Create splitter for resizable graphs
        self.splitter = QSplitter(Qt.Vertical)
        
        # Create initial graph(s) based on current_graph_count
        self._create_graphs(self.current_graph_count)
        
        self.layout.addWidget(self.splitter)
        self.setLayout(self.layout)
    
    def _create_graphs(self, count: int):
        """
        Create the specified number of graphs.
        
        Args:
            count: Number of graphs to create
        """
        # Clear existing graphs
        for widget in self.plot_widgets:
            if widget:
                widget.setParent(None)
                widget.deleteLater()
        
        self.plot_widgets.clear()
        self.plot_items.clear()
        self.signal_info.clear()
        self.signal_data.clear()
        
        # Create new graphs
        for i in range(count):
            plot_widget = self._create_single_plot(i)
            self.plot_widgets.append(plot_widget)
            self.plot_items.append(None)
            self.signal_info.append(None)
            self.signal_data.append(None)
            self.splitter.addWidget(plot_widget)
    
    def _create_single_plot(self, index: int) -> pg.PlotWidget:
        """
        Create a single plot widget.
        
        Args:
            index: Index of the plot
            
        Returns:
            Configured PlotWidget
        """
        plot_widget = pg.PlotWidget()
        
        # Apply theme
        bg_color = '#1a1a1a' if self.is_dark_mode else 'w'
        fg_color = '#ffffff' if self.is_dark_mode else '#000000'
        
        plot_widget.setBackground(bg_color)
        plot_widget.showGrid(x=True, y=True, alpha=0.3)
        plot_widget.setLabel('left', 'Value', color=fg_color)
        plot_widget.setLabel('bottom', 'Time', units='s', color=fg_color)
        plot_widget.addLegend()
        
        # Enable mouse interaction and zoom
        plot_widget.setMouseEnabled(x=True, y=True)
        
        # Enable auto-range on Y axis
        plot_widget.enableAutoRange(axis='y', enable=True)
        
        # Link X axis to first plot for synchronization
        if index > 0 and self.plot_widgets:
            plot_widget.setXLink(self.plot_widgets[0])
        
        return plot_widget
    
    def set_graph_count(self, count: int):
        """
        Dynamically change the number of displayed graphs.
        
        Args:
            count: New number of graphs (1-10)
        """
        if count < 1 or count > 10:
            return
        
        if count == self.current_graph_count:
            return
        
        self.current_graph_count = count
        
        # Store current signal data before recreating graphs
        stored_data = []
        for i in range(len(self.signal_data)):
            if self.signal_data[i]:
                stored_data.append({
                    'time': self.signal_data[i]['time'],
                    'value': self.signal_data[i]['value'],
                    'info': self.signal_info[i]
                })
        
        # Recreate graphs
        self._create_graphs(count)
        
        # Restore signal data to new graphs
        for i, data in enumerate(stored_data):
            if i < count:
                self.plot_signal(i, data['time'], data['value'], data['info'])
    
    def set_theme(self, is_dark: bool):
        """
        Apply theme to all graphs.
        
        Args:
            is_dark: True for dark mode, False for light mode
        """
        self.is_dark_mode = is_dark
        
        # Update all plot widgets
        bg_color = '#1a1a1a' if is_dark else 'w'
        fg_color = '#ffffff' if is_dark else '#000000'
        
        for plot_widget in self.plot_widgets:
            if plot_widget:
                plot_widget.setBackground(bg_color)
                plot_widget.getAxis('left').setPen(fg_color)
                plot_widget.getAxis('bottom').setPen(fg_color)
                plot_widget.getAxis('left').setTextPen(fg_color)
                plot_widget.getAxis('bottom').setTextPen(fg_color)
    
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
            index: Graph index
            time_data: Time values array
            value_data: Signal values array
            signal_info: Dictionary with signal metadata (message, signal, unit)
        """
        if index >= len(self.plot_widgets):
            return
        
        plot_widget = self.plot_widgets[index]
        
        # Clear previous plot
        if index < len(self.plot_items) and self.plot_items[index]:
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
        
        # Store plot item and signal info
        if index < len(self.plot_items):
            self.plot_items[index] = plot_item
            self.signal_info[index] = signal_info
            self.signal_data[index] = {
                'time': time_data,
                'value': value_data
            }
        
        # Update axis label
        fg_color = '#ffffff' if self.is_dark_mode else '#000000'
        y_label = signal_info['signal']
        if signal_info['unit']:
            y_label += f" ({signal_info['unit']})"
        plot_widget.setLabel('left', y_label, color=fg_color)
    
    def clear_graph(self, index: int):
        """
        Clear a specific graph.
        
        Args:
            index: Graph index
        """
        if index >= len(self.plot_widgets):
            return
        
        plot_widget = self.plot_widgets[index]
        
        if index < len(self.plot_items) and self.plot_items[index]:
            plot_widget.removeItem(self.plot_items[index])
            self.plot_items[index] = None
        
        if index < len(self.signal_info):
            self.signal_info[index] = None
        if index < len(self.signal_data):
            self.signal_data[index] = None
        
        fg_color = '#ffffff' if self.is_dark_mode else '#000000'
        plot_widget.setLabel('left', 'Value', color=fg_color)
    
    def clear_all(self):
        """Clear all graphs."""
        for i in range(len(self.plot_widgets)):
            self.clear_graph(i)
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
            index: Graph index
            filepath: Path to save the image
            
        Returns:
            True if successful
        """
        if index >= len(self.plot_widgets):
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
    
    def get_current_graph_count(self) -> int:
        """Get the current number of graphs."""
        return self.current_graph_count
    
    def get_signal_data(self) -> Dict[str, Dict]:
        """
        Get all signal data currently displayed.
        
        Returns:
            Dictionary with signal data for statistics calculations
        """
        result = {}
        for i, info in enumerate(self.signal_info):
            if info and i < len(self.signal_data) and self.signal_data[i]:
                key = f"{info['message']}.{info['signal']}"
                result[key] = {
                    'time': self.signal_data[i]['time'],
                    'value': self.signal_data[i]['value'],
                    'unit': info.get('unit', ''),
                    'message': info['message'],
                    'signal': info['signal']
                }
        return result
