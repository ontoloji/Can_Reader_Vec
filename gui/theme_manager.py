"""
Theme Manager Module
Manages application themes (light/dark mode) and plot styles.
"""

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt


class ThemeManager:
    """Manager for application themes and plot styles."""
    
    @staticmethod
    def apply_dark_theme(app):
        """Apply dark theme to the application."""
        dark_palette = QPalette()
        
        # Window colors
        dark_palette.setColor(QPalette.Window, QColor(43, 43, 43))
        dark_palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        
        # Base colors
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
        
        # Text colors
        dark_palette.setColor(QPalette.Text, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        
        # Button colors
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        
        # Highlight colors
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)
        
        # Disabled colors
        dark_palette.setColor(QPalette.Disabled, QPalette.Text, QColor(127, 127, 127))
        dark_palette.setColor(QPalette.Disabled, QPalette.ButtonText, QColor(127, 127, 127))
        
        app.setPalette(dark_palette)
        
        # Stylesheet for menus and UI elements
        app.setStyleSheet("""
            QToolTip {
                color: #ffffff;
                background-color: #2a2a2a;
                border: 1px solid white;
            }
QTreeWidget {
    background-color: #1a1a1a;
    alternate-background-color: #2a2a2a;
    color: #ffffff;
    border: 1px solid #555555;
}
QTreeWidget::item {
    background-color: #1a1a1a;
    color: #ffffff;
}
QTreeWidget::item:selected {
    background-color: #2a82da;
    color: #ffffff;
}
QTreeWidget::item:hover {
    background-color: #2a2a2a;
}
QHeaderView::section {
    background-color: #2b2b2b;
    color: #ffffff;
    border: 1px solid #555555;
    padding: 4px;
}
            QMenuBar {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QMenuBar::item {
                background-color: #2b2b2b;
                color: #ffffff;
                padding: 5px 10px;
            }
            QMenuBar::item:selected {
                background-color: #3d3d3d;
            }
            QMenu {
                background-color: #2b2b2b;
                color: #ffffff;
                border: 1px solid #555555;
            }
            QMenu::item {
                background-color: #2b2b2b;
                color: #ffffff;
                padding: 5px 20px;
            }
            QMenu::item:selected {
                background-color: #3d3d3d;
            }
            QToolBar {
                background-color: #2b2b2b;
                color: #ffffff;
                border: none;
            }
            QToolButton {
                color: #ffffff;
                background-color: #2b2b2b;
            }
            QToolButton:hover {
                background-color: #3d3d3d;
            }
                        QDialog {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QMessageBox {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
            }
            QPushButton {
                background-color: #3d3d3d;
                color: #ffffff;
                border: 1px solid #555555;
                padding: 5px 15px;
                min-width: 60px;
            }
            QPushButton:hover {
                background-color: #4d4d4d;
            }
            QPushButton:pressed {
                background-color: #2d2d2d;
            }
            QLineEdit {
                background-color: #1a1a1a;
                color: #ffffff;
                border: 1px solid #555555;
                padding: 3px;
            }
                QSpinBox {
        background-color: #1a1a1a;
        color: #ffffff;
        border: 1px solid #555555;
        padding: 3px;
    }
    QSpinBox::up-button {
        background-color: #3d3d3d;
        border-left: 1px solid #555555;
    }
    QSpinBox::down-button {
        background-color: #3d3d3d;
        border-left: 1px solid #555555;
    }
    QSpinBox::up-button:hover {
        background-color: #4d4d4d;
    }
    QSpinBox::down-button:hover {
        background-color: #4d4d4d;
    }
    QSpinBox::up-arrow {
        image: none;
        border-left: 4px solid transparent;
        border-right: 4px solid transparent;
        border-bottom: 4px solid #ffffff;
        width: 0px;
        height: 0px;
    }
    QSpinBox::down-arrow {
        image: none;
        border-left: 4px solid transparent;
        border-right: 4px solid transparent;
        border-top: 4px solid #ffffff;
        width: 0px;
        height: 0px;
    }
        """)
    
    @staticmethod
    def apply_light_theme(app):
        """Apply light theme (system default)."""
        app.setPalette(QApplication.style().standardPalette())
        app.setStyleSheet("")
    
    @staticmethod
    def get_plot_style(is_dark):
        """Get pyqtgraph plot style for current theme."""
        if is_dark:
            return {
                'background': '#1a1a1a',
                'foreground': '#ffffff',
                'grid_alpha': 0.3
            }
        else:
            return {
                'background': 'w',
                'foreground': '#000000',
                'grid_alpha': 0.5
            }