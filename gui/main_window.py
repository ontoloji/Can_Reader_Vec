"""
Main Window Module
Main application window with menu bar, panels, and status bar.
"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QFileDialog,
    QMessageBox, QAction, QStatusBar, QSplitter, QDockWidget,
    QToolBar, QApplication
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from pathlib import Path

from gui.signal_selector import SignalSelector
from gui.graph_panel import GraphPanel
from gui.dialogs import AboutDialog, UserGuideDialog
from gui.cursor_manager import CursorManager
from gui.statistics_widget import StatisticsWidget
from gui.theme_manager import ThemeManager
from data import BLFReader, DBCParser, SignalProcessor
from utils import Workspace
from utils.config import *
from utils.csv_exporter import CSVExporter
from utils.partial_exporter import PartialDataExporter


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
        self.cursor_manager = None
        self.statistics_widget = None
        self.stats_dock = None
        
        # Theme state
        self.is_dark_mode = False
        
        self.init_ui()
        self.create_menus()
        self.create_toolbar()
        self.create_status_bar()
        self.create_statistics_dock()
        
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
        self.signal_selector.graph_count_changed.connect(self.on_graph_count_changed)
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
        
        # Initialize cursor manager
        self.cursor_manager = CursorManager(self.graph_panel.plot_widgets)
        self.cursor_manager.cursor_moved.connect(self.on_cursor_moved)
    
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
        
        # Export submenu
        export_menu = file_menu.addMenu('E&xport')
        
        export_action = QAction('Export &Graphs...', self)
        export_action.setShortcut('Ctrl+E')
        export_action.triggered.connect(self.export_graphs)
        export_menu.addAction(export_action)
        
        export_csv_action = QAction('Export to &CSV...', self)
        export_csv_action.setShortcut('Ctrl+Shift+C')
        export_csv_action.triggered.connect(self.export_to_csv)
        export_menu.addAction(export_csv_action)
        
        export_time_range_action = QAction('Export &Time Range...', self)
        export_time_range_action.triggered.connect(self.export_time_range)
        export_menu.addAction(export_time_range_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('E&xit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu('&View')
        
        # Dark mode toggle
        self.dark_mode_action = QAction('&Dark Mode', self)
        self.dark_mode_action.setCheckable(True)
        self.dark_mode_action.setChecked(False)
        self.dark_mode_action.triggered.connect(self.toggle_dark_mode)
        view_menu.addAction(self.dark_mode_action)
        
        view_menu.addSeparator()
        
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
    
    def create_toolbar(self):
        """Create toolbar with cursor controls."""
        toolbar = QToolBar('Cursor Tools')
        toolbar.setMovable(False)
        self.addToolBar(Qt.TopToolBarArea, toolbar)
        
        # Add Cursor 1 (Green)
        add_cursor1_action = QAction('Add Cursor 1 (Green)', self)
        add_cursor1_action.triggered.connect(self.add_cursor_1)
        toolbar.addAction(add_cursor1_action)
        
        # Add Cursor 2 (Red)
        add_cursor2_action = QAction('Add Cursor 2 (Red)', self)
        add_cursor2_action.triggered.connect(self.add_cursor_2)
        toolbar.addAction(add_cursor2_action)
        
        toolbar.addSeparator()
        
        # Remove All Cursors
        remove_cursors_action = QAction('Remove All Cursors', self)
        remove_cursors_action.triggered.connect(self.remove_all_cursors)
        toolbar.addAction(remove_cursors_action)
    
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
    
    def create_statistics_dock(self):
        """Create statistics dock widget."""
        self.statistics_widget = StatisticsWidget()
        
        self.stats_dock = QDockWidget('Cursor Statistics', self)
        self.stats_dock.setWidget(self.statistics_widget)
        self.stats_dock.setAllowedAreas(Qt.RightDockWidgetArea | Qt.BottomDockWidgetArea)
        
        # Add dock to right side
        self.addDockWidget(Qt.RightDockWidgetArea, self.stats_dock)
        
        # Initially hide the statistics dock
        self.stats_dock.hide()
    
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
            
            # Create workspace data with new settings
            workspace_data = Workspace.create_workspace_data(
                blf_path=self.blf_path,
                dbc_path=self.dbc_path,
                selected_signals=self.signal_selector.get_selected_signals(),
                view_range=self.graph_panel.get_view_range(),
                window_geometry={
                    'width': self.width(),
                    'height': self.height()
                },
                graph_count=self.graph_panel.get_current_graph_count(),
                dark_mode=self.is_dark_mode,
                cursor_positions=self.cursor_manager.get_cursor_positions()
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
                
                # Restore graph count
                if 'graph_count' in workspace_data:
                    graph_count = workspace_data['graph_count']
                    self.signal_selector.set_graph_count(graph_count)
                    self.graph_panel.set_graph_count(graph_count)
                
                # Restore dark mode
                if 'dark_mode' in workspace_data:
                    should_be_dark = workspace_data['dark_mode']
                    if should_be_dark != self.is_dark_mode:
                        self.toggle_dark_mode()
                
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
                
                # Restore cursor positions
                if 'cursor_positions' in workspace_data:
                    cursor_positions = workspace_data['cursor_positions']
                    colors = {1: '#00ff00', 2: '#ff0000'}
                    for cursor_id, position in cursor_positions.items():
                        cursor_id = int(cursor_id)  # JSON keys are strings
                        if cursor_id in colors:
                            self.cursor_manager.add_cursor(cursor_id, colors[cursor_id], position)
                    if cursor_positions:
                        self.stats_dock.show()
                        self.update_statistics()
                
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
    
    def on_graph_count_changed(self, count: int):
        """
        Handle graph count change.
        
        Args:
            count: New number of graphs
        """
        self.graph_panel.set_graph_count(count)
        
        # Update cursor manager with new plot widgets
        self.cursor_manager.update_plot_widgets(self.graph_panel.plot_widgets)
        
        # Re-plot selected signals
        selected_signals = self.signal_selector.get_selected_signals()
        if selected_signals and self.signal_processor:
            self.on_signal_selection_changed(selected_signals)
    
    def toggle_dark_mode(self):
        """Toggle between dark and light mode."""
        self.is_dark_mode = not self.is_dark_mode
        
        app = QApplication.instance()
        if self.is_dark_mode:
            ThemeManager.apply_dark_theme(app)
        else:
            ThemeManager.apply_light_theme(app)
        
        # Update graph panel theme
        self.graph_panel.set_theme(self.is_dark_mode)
        
        # Update dark mode action state
        self.dark_mode_action.setChecked(self.is_dark_mode)
    
    def add_cursor_1(self):
        """Add cursor 1 (green) to all graphs."""
        if not self.cursor_manager.has_cursor(1):
            # Get middle of current view range
            view_range = self.graph_panel.get_view_range()
            position = (view_range['x_min'] + view_range['x_max']) / 2
            
            self.cursor_manager.add_cursor(1, '#00ff00', position)
            self.stats_dock.show()
            self.update_statistics()
        else:
            QMessageBox.information(
                self,
                'Cursor Exists',
                'Cursor 1 is already active.'
            )
    
    def add_cursor_2(self):
        """Add cursor 2 (red) to all graphs."""
        if not self.cursor_manager.has_cursor(2):
            # Get middle of current view range, offset a bit
            view_range = self.graph_panel.get_view_range()
            position = (view_range['x_min'] + view_range['x_max']) / 2
            position += (view_range['x_max'] - view_range['x_min']) * 0.1
            
            self.cursor_manager.add_cursor(2, '#ff0000', position)
            self.stats_dock.show()
            self.update_statistics()
        else:
            QMessageBox.information(
                self,
                'Cursor Exists',
                'Cursor 2 is already active.'
            )
    
    def remove_all_cursors(self):
        """Remove all cursors from graphs."""
        self.cursor_manager.remove_all_cursors()
        self.stats_dock.hide()
        self.statistics_widget.clear_statistics()
    
    def on_cursor_moved(self, cursor_id: int, position: float):
        """
        Handle cursor movement.
        
        Args:
            cursor_id: ID of the cursor that moved
            position: New position of the cursor
        """
        self.update_statistics()
    
    def update_statistics(self):
        """Update statistics widget with current cursor positions and signal data."""
        cursor_positions = self.cursor_manager.get_cursor_positions()
        signal_data = self.graph_panel.get_signal_data()
        
        self.statistics_widget.update_statistics(cursor_positions, signal_data)
    
    def export_to_csv(self):
        """Export selected signals to CSV file."""
        signal_data = self.graph_panel.get_signal_data()
        
        if not signal_data:
            QMessageBox.warning(
                self,
                'No Data',
                'Please select some signals before exporting to CSV.'
            )
            return
        
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            'Export to CSV',
            '',
            'CSV Files (*.csv);;All Files (*)'
        )
        
        if filepath:
            # Ensure .csv extension
            if not filepath.endswith('.csv'):
                filepath += '.csv'
            
            # Check if cursors are active for partial export
            cursor_positions = self.cursor_manager.get_cursor_positions()
            time_range = None
            
            if len(cursor_positions) == 2:
                positions = sorted(cursor_positions.values())
                reply = QMessageBox.question(
                    self,
                    'Export Range',
                    'Two cursors are active. Export only the data between cursors?',
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.Yes
                )
                if reply == QMessageBox.Yes:
                    time_range = (positions[0], positions[1])
            
            # Export
            if CSVExporter.export_signals(filepath, signal_data, time_range):
                QMessageBox.information(
                    self,
                    'Success',
                    'Data exported to CSV successfully!'
                )
            else:
                QMessageBox.critical(
                    self,
                    'Error',
                    'Failed to export data to CSV.'
                )
    
    def export_time_range(self):
        """Export partial data (time range) to JSON file."""
        signal_data = self.graph_panel.get_signal_data()
        
        if not signal_data:
            QMessageBox.warning(
                self,
                'No Data',
                'Please select some signals before exporting.'
            )
            return
        
        cursor_positions = self.cursor_manager.get_cursor_positions()
        
        if len(cursor_positions) < 2:
            QMessageBox.warning(
                self,
                'Need Cursors',
                'Please add two cursors to define the time range to export.'
            )
            return
        
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            'Export Time Range',
            '',
            'JSON Files (*.json);;All Files (*)'
        )
        
        if filepath:
            # Ensure .json extension
            if not filepath.endswith('.json'):
                filepath += '.json'
            
            # Get time range from cursors
            positions = sorted(cursor_positions.values())
            time_range = (positions[0], positions[1])
            
            # Metadata
            metadata = {
                'blf_file': Path(self.blf_path).name if self.blf_path else '',
                'dbc_file': Path(self.dbc_path).name if self.dbc_path else ''
            }
            
            # Export
            if PartialDataExporter.export_time_range(filepath, signal_data, time_range, metadata):
                QMessageBox.information(
                    self,
                    'Success',
                    f'Time range exported successfully!\n'
                    f'Duration: {time_range[1] - time_range[0]:.3f}s'
                )
            else:
                QMessageBox.critical(
                    self,
                    'Error',
                    'Failed to export time range.'
                )
