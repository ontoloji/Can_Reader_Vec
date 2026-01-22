#!/usr/bin/env python3
"""
CAN Data Viewer Application
Main entry point for the application.
"""

import sys
from PyQt5.QtWidgets import QApplication
from gui import MainWindow


def main():
    """Main application entry point."""
    app = QApplication(sys.argv)
    app.setApplicationName("CAN Data Viewer")
    app.setOrganizationName("CAN Tools")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    # Run application
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
