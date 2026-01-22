"""
Dialogs Module
Various dialogs for export, workspace operations, etc.
"""

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton
from PyQt5.QtCore import Qt


class AboutDialog(QDialog):
    """About dialog showing application information."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About CAN Data Viewer")
        self.setModal(True)
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout()
        
        # Application info
        info_text = """
        <h2>CAN Data Viewer</h2>
        <p><b>Version:</b> 1.0.0</p>
        <p>A graphical application for visualizing CAN data from BLF files using DBC definitions.</p>
        
        <p><b>Features:</b></p>
        <ul>
            <li>Read BLF (Binary Logging Format) files</li>
            <li>Parse DBC (CAN Database) files</li>
            <li>Display up to 5 signals simultaneously</li>
            <li>Synchronized zoom and pan across graphs</li>
            <li>Export graphs to PNG, JPEG, SVG</li>
            <li>Save and load workspace configurations</li>
        </ul>
        
        <p><b>Technologies:</b></p>
        <ul>
            <li>Python with PyQt5</li>
            <li>python-can for BLF reading</li>
            <li>cantools for DBC parsing</li>
            <li>pyqtgraph for high-performance plotting</li>
        </ul>
        """
        
        info_label = QLabel(info_text)
        info_label.setWordWrap(True)
        info_label.setTextFormat(Qt.RichText)
        layout.addWidget(info_label)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)
        self.setFixedSize(500, 450)


class UserGuideDialog(QDialog):
    """User guide dialog with usage instructions."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("User Guide")
        self.setModal(True)
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout()
        
        # Guide text
        guide_text = """
<h2>User Guide</h2>

<h3>Getting Started</h3>
<ol>
    <li><b>Open BLF File:</b> File → Open BLF File, select your BLF file</li>
    <li><b>Open DBC File:</b> File → Open DBC File, select your DBC file</li>
    <li><b>Select Signals:</b> In the left panel, check the signals you want to visualize (max 5)</li>
    <li><b>View Graphs:</b> Selected signals are automatically plotted in the right panel</li>
</ol>

<h3>Navigation</h3>
<ul>
    <li><b>Zoom In:</b> Scroll up with mouse wheel or drag to select area</li>
    <li><b>Zoom Out:</b> Scroll down with mouse wheel</li>
    <li><b>Pan:</b> Right-click and drag to pan</li>
    <li><b>Reset View:</b> View → Reset Zoom</li>
</ul>

<h3>Export</h3>
<ul>
    <li><b>Export Graphs:</b> File → Export Graphs</li>
    <li>Choose format: PNG, JPEG, or SVG</li>
    <li>All graphs will be saved as separate files</li>
</ul>

<h3>Workspace</h3>
<ul>
    <li><b>Save Workspace:</b> File → Save Workspace</li>
    <li>Saves current file paths, selected signals, and view settings</li>
    <li><b>Load Workspace:</b> File → Load Workspace</li>
    <li>Restores a previously saved workspace</li>
</ul>

<h3>Tips</h3>
<ul>
    <li>All graphs are synchronized on the X-axis (time)</li>
    <li>Grayed out signals are not available in the BLF file</li>
    <li>Use the status bar to see file information</li>
</ul>
        """
        
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setHtml(guide_text)
        layout.addWidget(text_edit)
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)
        self.resize(600, 500)
