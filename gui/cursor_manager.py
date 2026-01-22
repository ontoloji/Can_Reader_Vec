"""
Cursor Manager Module
Manages multiple cursors across synchronized graphs.
"""

from pyqtgraph import InfiniteLine
from PyQt5.QtCore import pyqtSignal, QObject, Qt
from typing import List, Dict


class CursorManager(QObject):
    """Manager for synchronized cursors across multiple graphs."""
    
    # Signal emitted when cursor position changes
    cursor_moved = pyqtSignal(int, float)  # cursor_id, position
    
    def __init__(self, plot_widgets):
        """
        Initialize cursor manager.
        
        Args:
            plot_widgets: List of PlotWidget instances to manage cursors for
        """
        super().__init__()
        self.plot_widgets = plot_widgets  # List of PlotWidget objects
        self.cursors: Dict[int, List[InfiniteLine]] = {}  # {cursor_id: [line1, line2, ...]}
    
    def update_plot_widgets(self, plot_widgets):
        """
        Update the list of plot widgets (for dynamic graph count changes).
        
        Args:
            plot_widgets: New list of PlotWidget instances
        """
        # Store current cursor positions
        positions = self.get_cursor_positions()
        
        # Remove all cursors from old plots
        cursor_ids = list(self.cursors.keys())
        for cursor_id in cursor_ids:
            self.remove_cursor(cursor_id)
        
        # Update plot widgets
        self.plot_widgets = plot_widgets
        
        # Re-add cursors to new plots
        colors = {1: '#00ff00', 2: '#ff0000'}  # Green for cursor 1, Red for cursor 2
        for cursor_id, position in positions.items():
            if cursor_id in colors:
                self.add_cursor(cursor_id, colors[cursor_id], position)
    
    def add_cursor(self, cursor_id: int, color: str, position: float = 0):
        """
        Add a cursor to all graphs.
        
        Args:
            cursor_id: Unique identifier for the cursor (1 or 2)
            color: Color of the cursor line (e.g., '#00ff00' for green)
            position: Initial X position of the cursor
        """
        if cursor_id in self.cursors:
            return  # Cursor already exists
        
        cursor_lines = []
        for plot_widget in self.plot_widgets:
            # Create infinite line
            line = InfiniteLine(
                pos=position,
                angle=90,
                pen={'color': color, 'width': 2, 'style': Qt.DashLine},
                movable=True
            )
            
            # Add to plot
            plot_widget.addItem(line)
            
            # Connect signal for synchronization
            line.sigPositionChanged.connect(
                lambda ln=line, cid=cursor_id: self._on_cursor_moved(cid, ln)
            )
            
            cursor_lines.append(line)
        
        self.cursors[cursor_id] = cursor_lines
    
    def remove_cursor(self, cursor_id: int):
        """
        Remove a cursor from all graphs.
        
        Args:
            cursor_id: Identifier of the cursor to remove
        """
        if cursor_id not in self.cursors:
            return
        
        for line in self.cursors[cursor_id]:
            # Get the plot item and remove the line
            plot_item = line.getViewBox()
            if plot_item:
                plot_item.removeItem(line)
        
        del self.cursors[cursor_id]
    
    def remove_all_cursors(self):
        """Remove all cursors from all graphs."""
        cursor_ids = list(self.cursors.keys())
        for cursor_id in cursor_ids:
            self.remove_cursor(cursor_id)
    
    def _on_cursor_moved(self, cursor_id: int, moved_line: InfiniteLine):
        """
        Handle cursor movement - synchronize across all graphs.
        
        Args:
            cursor_id: ID of the cursor that moved
            moved_line: The InfiniteLine object that was moved
        """
        new_pos = moved_line.value()
        
        # Update all other lines with the same cursor_id
        if cursor_id in self.cursors:
            for line in self.cursors[cursor_id]:
                if line != moved_line:
                    # Block signals to prevent recursive updates
                    line.blockSignals(True)
                    line.setValue(new_pos)
                    line.blockSignals(False)
        
        # Emit signal for statistics update
        self.cursor_moved.emit(cursor_id, new_pos)
    
    def get_cursor_positions(self) -> Dict[int, float]:
        """
        Get current positions of all cursors.
        
        Returns:
            Dictionary mapping cursor_id to position
        """
        positions = {}
        for cursor_id, lines in self.cursors.items():
            if lines:
                positions[cursor_id] = lines[0].value()
        return positions
    
    def has_cursor(self, cursor_id: int) -> bool:
        """
        Check if a cursor exists.
        
        Args:
            cursor_id: ID of the cursor to check
            
        Returns:
            True if cursor exists
        """
        return cursor_id in self.cursors
