"""
Main Window Module
Main application window with menu bar, panels, and status bar.
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QFileDialog,
    QMessageBox, QAction, QStatusBar, QSplitter
)
from PyQt5.QtCore import Qt
from pathlib import Path

from gui.signal_selector import SignalSelector
from gui.graph_panel import GraphPanel
from gui.dialogs import AboutDialog, UserGuideDialog
from data import BLFReader, DBCParser, SignalProcessor
from utils import Workspace
from utils.config import *


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        
        # Data objects
        self.blf_reader = BLFReader()
        self.dbc_parser = DBCParser()
        self.signal_processor = None
        
        # File paths
        self.blf_path = ""
        self.dbc_path = ""
        
        # UI components
        self.signal_selector = None
        self.graph_panel = None
        
        self.init_ui()
        self.create_menus()
        self.create_status_bar()
        
        # Set minimum size
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        self.resize(1200, 800)
    
    def init_ui(self):
        """Initialize the user interface."""
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout with splitter
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel - Signal selector
        self.signal_selector = SignalSelector(max_signals=MAX_SIGNALS)
        self.signal_selector.selection_changed.connect(self.on_signal_selection_changed)
        self.signal_selector.setMinimumWidth(SIGNAL_PANEL_WIDTH)
        splitter.addWidget(self.signal_selector)
        
        # Right panel - Graphs
        self.graph_panel = GraphPanel(max_graphs=MAX_SIGNALS, colors=GRAPH_COLORS)
        splitter.addWidget(self.graph_panel)
        
        # Set splitter sizes (25% left, 75% right)
        splitter.setSizes([300, 900])
        
        # Add splitter to layout
        layout = QHBoxLayout()
        layout.addWidget(splitter)
        central_widget.setLayout(layout)
    
    def create_menus(self):
        """Create menu bar and menus."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('&File')
        
        open_blf_action = QAction('Open &BLF File...', self)
        open_blf_action.setShortcut('Ctrl+B')
        open_blf_action.triggered.connect(self.open_blf_file)
        file_menu.addAction(open_blf_action)
        
        open_dbc_action = QAction('Open &DBC File...', self)
        open_dbc_action.setShortcut('Ctrl+D')
        open_dbc_action.triggered.connect(self.open_dbc_file)
        file_menu.addAction(open_dbc_action)
        
        file_menu.addSeparator()
        
        save_workspace_action = QAction('&Save Workspace...', self)
        save_workspace_action.setShortcut('Ctrl+S')
        save_workspace_action.triggered.connect(self.save_workspace)
        file_menu.addAction(save_workspace_action)
        
        load_workspace_action = QAction('&Load Workspace...', self)
        load_workspace_action.setShortcut('Ctrl+L')
        load_workspace_action.triggered.connect(self.load_workspace)
        file_menu.addAction(load_workspace_action)
        
        file_menu.addSeparator()
        
        export_action = QAction('&Export Graphs...', self)
        export_action.setShortcut('Ctrl+E')
        export_action.triggered.connect(self.export_graphs)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('E&xit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu('&View')
        
        reset_zoom_action = QAction('&Reset Zoom', self)
        reset_zoom_action.setShortcut('Ctrl+R')
        reset_zoom_action.triggered.connect(self.graph_panel.reset_zoom)
        view_menu.addAction(reset_zoom_action)
        
        fit_data_action = QAction('&Fit to Data', self)
        fit_data_action.setShortcut('Ctrl+F')
        fit_data_action.triggered.connect(self.graph_panel.fit_to_data)
        view_menu.addAction(fit_data_action)
        
        # Help menu
        help_menu = menubar.addMenu('&Help')
        
        user_guide_action = QAction('&User Guide', self)
        user_guide_action.setShortcut('F1')
        user_guide_action.triggered.connect(self.show_user_guide)
        help_menu.addAction(user_guide_action)
        
        about_action = QAction('&About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_status_bar(self):
        """Create status bar."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.update_status_bar()
    
    def update_status_bar(self):
        """Update status bar with current file information."""
        status_parts = []
        
        if self.blf_path:
            blf_info = self.blf_reader.get_file_info()
            blf_name = Path(self.blf_path).name
            status_parts.append(
                f"BLF: {blf_name} ({blf_info['message_count']} msgs, "
                f"{blf_info['duration']:.1f}s)"
            )
        else:
            status_parts.append("BLF: Not loaded")
        
        if self.dbc_path:
            dbc_info = self.dbc_parser.get_file_info()
            dbc_name = Path(self.dbc_path).name
            status_parts.append(
                f"DBC: {dbc_name} ({dbc_info['message_count']} msgs)"
            )
        else:
            status_parts.append("DBC: Not loaded")
        
        selected_count = len(self.signal_selector.get_selected_signals())
        status_parts.append(f"Selected: {selected_count}/{MAX_SIGNALS}")
        
        self.status_bar.showMessage(" | ".join(status_parts))
    
    def open_blf_file(self):
        """Open and load a BLF file."""
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Open BLF File",
            "",
            BLF_FILTER
        )
        
        if filepath:
            if self.blf_reader.load_file(filepath):
                self.blf_path = filepath
                QMessageBox.information(
                    self,
                    "Success",
                    "BLF file loaded successfully!"
                )
                self.update_status_bar()
                self.refresh_signal_list()
            else:
                QMessageBox.critical(
                    self,
                    "Error",
                    "Failed to load BLF file. Please check the file format."
                )
    
    def open_dbc_file(self):
        """Open and load a DBC file."""
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Open DBC File",
            "",
            DBC_FILTER
        )
        
        if filepath:
            if self.dbc_parser.load_file(filepath):
                self.dbc_path = filepath
                QMessageBox.information(
                    self,
                    "Success",
                    "DBC file loaded successfully!"
                )
                self.update_status_bar()
                self.refresh_signal_list()
            else:
                QMessageBox.critical(
                    self,
                    "Error",
                    "Failed to load DBC file. Please check the file format."
                )
    
    def refresh_signal_list(self):
        """Refresh the signal list in the selector."""
        if self.dbc_path and self.blf_path:
            # Create signal processor
            self.signal_processor = SignalProcessor(self.blf_reader, self.dbc_parser)
            
            # Get messages from DBC and available IDs from BLF
            messages = self.dbc_parser.get_messages()
            available_ids = self.blf_reader.get_unique_message_ids()
            
            # Load into signal selector
            self.signal_selector.load_messages(messages, available_ids)
    
    def on_signal_selection_changed(self, selected_signals):
        """Handle signal selection changes."""
        if not self.signal_processor:
            return
        
        # Clear all graphs
        self.graph_panel.clear_all()
        
        # Plot each selected signal
        for i, sig_info in enumerate(selected_signals):
            result = self.signal_processor.process_signal(
                sig_info['message'],
                sig_info['signal']
            )
            
            if result:
                time_data, value_data = result
                self.graph_panel.plot_signal(i, time_data, value_data, sig_info)
        
        self.update_status_bar()
    
    def export_graphs(self):
        """Export all graphs to image files."""
        if not self.signal_selector.get_selected_signals():
            QMessageBox.warning(
                self,
                "No Signals",
                "Please select some signals before exporting."
            )
            return
        
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Export Graphs",
            "",
            "PNG Files (*.png);;JPEG Files (*.jpg);;SVG Files (*.svg)"
        )
        
        if filepath:
            if self.graph_panel.export_all(filepath):
                QMessageBox.information(
                    self,
                    "Success",
                    "Graphs exported successfully!"
                )
            else:
                QMessageBox.critical(
                    self,
                    "Error",
                    "Failed to export graphs."
                )
    
    def save_workspace(self):
        """Save current workspace to a file."""
        if not self.blf_path or not self.dbc_path:
            QMessageBox.warning(
                self,
                "No Files Loaded",
                "Please load BLF and DBC files before saving workspace."
            )
            return
        
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Save Workspace",
            "",
            WORKSPACE_FILTER
        )
        
        if filepath:
            # Ensure .workspace extension
            if not filepath.endswith(WORKSPACE_EXTENSION):
                filepath += WORKSPACE_EXTENSION
            
            # Create workspace data
            workspace_data = Workspace.create_workspace_data(
                blf_path=self.blf_path,
                dbc_path=self.dbc_path,
                selected_signals=self.signal_selector.get_selected_signals(),
                view_range=self.graph_panel.get_view_range(),
                window_geometry={
                    'width': self.width(),
                    'height': self.height()
                }
            )
            
            if Workspace.save(filepath, workspace_data):
                QMessageBox.information(
                    self,
                    "Success",
                    "Workspace saved successfully!"
                )
            else:
                QMessageBox.critical(
                    self,
                    "Error",
                    "Failed to save workspace."
                )
    
    def load_workspace(self):
        """Load workspace from a file."""
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Load Workspace",
            "",
            WORKSPACE_FILTER
        )
        
        if filepath:
            workspace_data = Workspace.load(filepath)
            
            if workspace_data:
                # Load BLF file
                if 'blf_path' in workspace_data:
                    if self.blf_reader.load_file(workspace_data['blf_path']):
                        self.blf_path = workspace_data['blf_path']
                
                # Load DBC file
                if 'dbc_path' in workspace_data:
                    if self.dbc_parser.load_file(workspace_data['dbc_path']):
                        self.dbc_path = workspace_data['dbc_path']
                
                # Refresh signal list
                self.refresh_signal_list()
                
                # Restore selected signals
                if 'selected_signals' in workspace_data:
                    self.signal_selector.set_selected_signals(
                        workspace_data['selected_signals']
                    )
                
                # Restore view range
                if 'view_range' in workspace_data:
                    view_range = workspace_data['view_range']
                    self.graph_panel.set_view_range(
                        view_range['x_min'],
                        view_range['x_max']
                    )
                
                # Restore window geometry
                if 'window_geometry' in workspace_data:
                    geom = workspace_data['window_geometry']
                    self.resize(geom['width'], geom['height'])
                
                self.update_status_bar()
                
                QMessageBox.information(
                    self,
                    "Success",
                    "Workspace loaded successfully!"
                )
            else:
                QMessageBox.critical(
                    self,
                    "Error",
                    "Failed to load workspace."
                )
    
    def show_about(self):
        """Show about dialog."""
        dialog = AboutDialog(self)
        dialog.exec_()
    
    def show_user_guide(self):
        """Show user guide dialog."""
        dialog = UserGuideDialog(self)
        dialog.exec_()
