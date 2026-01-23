"""
Raw Data Viewer Dialog
Displays BLF raw data in hexadecimal format without DBC decoding.
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QLabel, QSpinBox,
    QFileDialog, QMessageBox, QHeaderView, QProgressBar
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import csv


class RawDataViewerDialog(QDialog):
    """Dialog for viewing raw BLF data in hexadecimal format."""
    
    def __init__(self, blf_reader, parent=None):
        super().__init__(parent)
        self.blf_reader = blf_reader
        self.raw_data = []
        
        self.setWindowTitle("BLF Raw Data Viewer")
        self.resize(900, 600)
        
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout()
        
        # Top controls
        control_layout = QHBoxLayout()
        
        control_layout.addWidget(QLabel("Max Messages:"))
        
        self.max_messages_spin = QSpinBox()
        self.max_messages_spin.setMinimum(100)
        self.max_messages_spin.setMaximum(1000000)
        self.max_messages_spin.setValue(10000)
        self.max_messages_spin.setSingleStep(1000)
        control_layout.addWidget(self.max_messages_spin)
        
        reload_btn = QPushButton("Reload")
        reload_btn.clicked.connect(self.load_data)
        control_layout.addWidget(reload_btn)
        
        control_layout.addStretch()
        
        export_csv_btn = QPushButton("Export to CSV...")
        export_csv_btn.clicked.connect(self.export_to_csv)
        control_layout.addWidget(export_csv_btn)
        
        export_txt_btn = QPushButton("Export to TXT...")
        export_txt_btn.clicked.connect(self.export_to_txt)
        control_layout.addWidget(export_txt_btn)
        
        layout.addLayout(control_layout)
        
        # Info label
        self.info_label = QLabel("Loading data...")
        layout.addWidget(self.info_label)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Timestamp (s)", "Message ID (Hex)", "Message ID (Dec)", "DLC", "Data (Hex)"
        ])
        
        # Set column widths
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.Stretch)
        
        # Set font to monospace for hex data
        font = QFont("Courier New", 9)
        self.table.setFont(font)
        
        layout.addWidget(self.table)
        
        # Bottom buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def load_data(self):
        """Load raw data from BLF reader."""
        max_msg = self.max_messages_spin.value()
        
        self.info_label.setText(f"Loading up to {max_msg} messages...")
        self.progress_bar.setVisible(True)
        self.progress_bar.setMaximum(0)  # Indeterminate
        
        # Process events to update UI
        from PyQt5.QtWidgets import QApplication
        QApplication.processEvents()
        
        # Get raw data
        self.raw_data = self.blf_reader.get_raw_messages(max_messages=max_msg)
        
        # Populate table
        self.populate_table()
        
        self.progress_bar.setVisible(False)
        
        # Update info
        blf_info = self.blf_reader.get_file_info()
        total = blf_info['message_count']
        loaded = len(self.raw_data)
        self.info_label.setText(
            f"Showing {loaded:,} of {total:,} messages "
            f"({loaded/total*100:.1f}%)"
        )
    
    def populate_table(self):
        """Populate table with raw data."""
        self.table.setRowCount(len(self.raw_data))
        
        for row, msg_data in enumerate(self.raw_data):
            # Timestamp
            item = QTableWidgetItem(f"{msg_data['timestamp']:.6f}")
            item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row, 0, item)
            
            # ID (Hex)
            item = QTableWidgetItem(msg_data['id_hex'])
            item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 1, item)
            
            # ID (Dec)
            item = QTableWidgetItem(str(msg_data['id']))
            item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 2, item)
            
            # DLC
            item = QTableWidgetItem(str(msg_data['dlc']))
            item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 3, item)
            
            # Data (Hex)
            item = QTableWidgetItem(msg_data['data_hex'])
            self.table.setItem(row, 4, item)
    
    def export_to_csv(self):
        """Export raw data to CSV file."""
        if not self.raw_data:
            QMessageBox.warning(self, "No Data", "No data to export.")
            return
        
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Export Raw Data to CSV",
            "blf_raw_data.csv",
            "CSV Files (*.csv);;All Files (*)"
        )
        
        if not filepath:
            return
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Header
                writer.writerow([
                    'Timestamp (s)',
                    'Message ID (Hex)',
                    'Message ID (Dec)',
                    'DLC',
                    'Data (Hex)'
                ])
                
                # Data
                for msg in self.raw_data:
                    writer.writerow([
                        f"{msg['timestamp']:.6f}",
                        msg['id_hex'],
                        msg['id'],
                        msg['dlc'],
                        msg['data_hex']
                    ])
            
            QMessageBox.information(
                self,
                "Success",
                f"Raw data exported successfully!\n{len(self.raw_data)} messages written."
            )
        
        except Exception as e:
            QMessageBox.critical(
                self,
                "Export Error",
                f"Failed to export data:\n{str(e)}"
            )
    
    def export_to_txt(self):
        """Export raw data to text file."""
        if not self.raw_data:
            QMessageBox.warning(self, "No Data", "No data to export.")
            return
        
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Export Raw Data to TXT",
            "blf_raw_data.txt",
            "Text Files (*.txt);;All Files (*)"
        )
        
        if not filepath:
            return
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                # Header
                f.write("BLF Raw Data (Hexadecimal Format)\n")
                f.write("=" * 80 + "\n\n")
                
                f.write(f"{'Timestamp':>12}  {'ID (Hex)':>10}  {'ID (Dec)':>8}  {'DLC':>3}  {'Data (Hex)'}\n")
                f.write("-" * 80 + "\n")
                
                # Data
                for msg in self.raw_data:
                    f.write(
                        f"{msg['timestamp']:>12.6f}  "
                        f"{msg['id_hex']:>10}  "
                        f"{msg['id']:>8}  "
                        f"{msg['dlc']:>3}  "
                        f"{msg['data_hex']}\n"
                    )
                
                f.write("\n" + "=" * 80 + "\n")
                f.write(f"Total Messages: {len(self.raw_data)}\n")
            
            QMessageBox.information(
                self,
                "Success",
                f"Raw data exported successfully!\n{len(self.raw_data)} messages written."
            )
        
        except Exception as e:
            QMessageBox.critical(
                self,
                "Export Error",
                f"Failed to export data:\n{str(e)}"
            )