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
    def apply_dark_theme(app: QApplication):
        """
        Apply dark theme to the application.
        
        Args:
            app: QApplication instance
        """
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
        
        # Set stylesheet for better look
        app.setStyleSheet("""
            QToolTip {
                color: #ffffff;
                background-color: #2a2a2a;
                border: 1px solid white;
            }
            QTreeWidget {
                background-color: #1a1a1a;
                alternate-background-color: #2a2a2a;
            }
        """)
    
    @staticmethod
    def apply_light_theme(app: QApplication):
        """
        Apply light theme to the application (system default).
        
        Args:
            app: QApplication instance
        """
        # Reset to default palette
        app.setPalette(QApplication.style().standardPalette())
        app.setStyleSheet("")  # Clear custom stylesheet
    
    @staticmethod
    def get_plot_style(is_dark: bool) -> dict:
        """
        Get pyqtgraph plot style for current theme.
        
        Args:
            is_dark: True for dark theme, False for light theme
            
        Returns:
            Dictionary with plot style parameters
        """
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
