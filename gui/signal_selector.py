"""
Signal Selector Widget
Left panel for selecting CAN messages and signals.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem,
    QPushButton, QLabel, QMessageBox
)
from PyQt5.QtCore import pyqtSignal, Qt
from typing import List, Dict, Any, Optional


class SignalSelector(QWidget):
    """Widget for selecting CAN signals from a tree view."""
    
    # Signal emitted when selection changes
    selection_changed = pyqtSignal(list)
    
    def __init__(self, max_signals: int = 5):
        super().__init__()
        self.max_signals = max_signals
        self.selected_signals: List[Dict[str, str]] = []
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout()
        
        # Title label
        title_label = QLabel("Signal Selection")
        title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title_label)
        
        # Tree widget for messages and signals
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Message / Signal", "ID / Unit"])
        self.tree.itemChanged.connect(self.on_item_changed)
        layout.addWidget(self.tree)
        
        # Selected signals label
        self.selected_label = QLabel(f"Selected: 0/{self.max_signals}")
        layout.addWidget(self.selected_label)
        
        # Clear selection button
        clear_btn = QPushButton("Clear Selection")
        clear_btn.clicked.connect(self.clear_selection)
        layout.addWidget(clear_btn)
        
        self.setLayout(layout)
    
    def load_messages(self, messages: List[Dict[str, Any]], available_ids: List[int]):
        """
        Load messages from DBC and highlight those available in BLF.
        
        Args:
            messages: List of message dictionaries from DBC parser
            available_ids: List of message IDs available in BLF file
        """
        self.tree.clear()
        self.tree.setColumnWidth(0, 200)
        
        available_id_set = set(available_ids)
        
        for msg in messages:
            msg_id = msg['id']
            is_available = msg_id in available_id_set
            
            # Create message item
            msg_item = QTreeWidgetItem(self.tree)
            msg_item.setText(0, msg['name'])
            msg_item.setText(1, f"0x{msg_id:X}")
            msg_item.setData(0, Qt.UserRole, {'type': 'message', 'name': msg['name'], 'id': msg_id})
            
            # Gray out unavailable messages
            if not is_available:
                for col in range(2):
                    msg_item.setForeground(col, Qt.gray)
                msg_item.setToolTip(0, "Not available in BLF file")
            
            # Add signal items
            for sig in msg['signals']:
                sig_item = QTreeWidgetItem(msg_item)
                sig_item.setText(0, sig['name'])
                sig_item.setText(1, sig['unit'])
                sig_item.setData(0, Qt.UserRole, {
                    'type': 'signal',
                    'message': msg['name'],
                    'name': sig['name'],
                    'unit': sig['unit']
                })
                
                # Only allow selection if message is available
                if is_available:
                    sig_item.setFlags(sig_item.flags() | Qt.ItemIsUserCheckable)
                    sig_item.setCheckState(0, Qt.Unchecked)
                else:
                    for col in range(2):
                        sig_item.setForeground(col, Qt.gray)
    
    def on_item_changed(self, item: QTreeWidgetItem, column: int):
        """Handle item check state changes."""
        data = item.data(0, Qt.UserRole)
        
        if data and data['type'] == 'signal':
            if item.checkState(0) == Qt.Checked:
                # Check if we can add more signals
                if len(self.selected_signals) >= self.max_signals:
                    item.setCheckState(0, Qt.Unchecked)
                    QMessageBox.warning(
                        self,
                        "Maximum Signals",
                        f"Maximum {self.max_signals} signals can be selected."
                    )
                    return
                
                # Add to selected signals
                signal_info = {
                    'message': data['message'],
                    'signal': data['name'],
                    'unit': data['unit']
                }
                self.selected_signals.append(signal_info)
            else:
                # Remove from selected signals
                signal_info = {
                    'message': data['message'],
                    'signal': data['name'],
                    'unit': data['unit']
                }
                if signal_info in self.selected_signals:
                    self.selected_signals.remove(signal_info)
            
            # Update label and emit signal
            self.update_selection_label()
            self.selection_changed.emit(self.selected_signals)
    
    def clear_selection(self):
        """Clear all selected signals."""
        # Uncheck all items
        for i in range(self.tree.topLevelItemCount()):
            msg_item = self.tree.topLevelItem(i)
            for j in range(msg_item.childCount()):
                sig_item = msg_item.child(j)
                sig_item.setCheckState(0, Qt.Unchecked)
        
        self.selected_signals.clear()
        self.update_selection_label()
        self.selection_changed.emit(self.selected_signals)
    
    def update_selection_label(self):
        """Update the selected signals count label."""
        self.selected_label.setText(
            f"Selected: {len(self.selected_signals)}/{self.max_signals}"
        )
    
    def get_selected_signals(self) -> List[Dict[str, str]]:
        """Get the list of selected signals."""
        return self.selected_signals
    
    def set_selected_signals(self, signals: List[Dict[str, str]]):
        """
        Set selected signals (used when loading workspace).
        
        Args:
            signals: List of signal dictionaries
        """
        self.clear_selection()
        
        # Find and check the items
        for sig_info in signals:
            if len(self.selected_signals) >= self.max_signals:
                break
            
            for i in range(self.tree.topLevelItemCount()):
                msg_item = self.tree.topLevelItem(i)
                msg_data = msg_item.data(0, Qt.UserRole)
                
                if msg_data and msg_data['name'] == sig_info['message']:
                    for j in range(msg_item.childCount()):
                        sig_item = msg_item.child(j)
                        sig_data = sig_item.data(0, Qt.UserRole)
                        
                        if sig_data and sig_data['name'] == sig_info['signal']:
                            sig_item.setCheckState(0, Qt.Checked)
                            break
                    break
