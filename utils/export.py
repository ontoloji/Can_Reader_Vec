"""
Export Module
Handles exporting graphs to various image formats.
"""

from typing import List, Optional
from pathlib import Path
import pyqtgraph.exporters as exporters


class GraphExporter:
    """Class for exporting graphs to image files."""
    
    @staticmethod
    def export_graph(plot_widget, filepath: str, width: int = 1920, height: int = 1080) -> bool:
        """
        Export a single graph to an image file.
        
        Args:
            plot_widget: PyQtGraph PlotWidget to export
            filepath: Path to save the image
            width: Image width in pixels (used for PNG/JPEG export)
            height: Image height in pixels (used for PNG/JPEG export)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            file_ext = Path(filepath).suffix.lower()
            
            if file_ext in ['.png', '.jpg', '.jpeg']:
                exporter = exporters.ImageExporter(plot_widget.plotItem)
                # Set both width and height parameters
                params = exporter.parameters()
                params['width'] = width
                params['height'] = height
                exporter.export(filepath)
            elif file_ext == '.svg':
                exporter = exporters.SVGExporter(plot_widget.plotItem)
                exporter.export(filepath)
            else:
                print(f"Unsupported export format: {file_ext}")
                return False
            
            return True
        except Exception as e:
            print(f"Error exporting graph: {e}")
            return False
    
    @staticmethod
    def export_all_graphs(
        plot_widgets: List,
        base_filepath: str,
        width: int = 1920,
        height: int = 1080
    ) -> bool:
        """
        Export all graphs to separate files.
        
        Args:
            plot_widgets: List of PlotWidgets to export
            base_filepath: Base filepath (without extension)
            width: Image width in pixels
            height: Image height in pixels
            
        Returns:
            True if all exports successful, False otherwise
        """
        try:
            base_path = Path(base_filepath)
            extension = base_path.suffix
            stem = base_path.stem
            parent = base_path.parent
            
            success = True
            for i, widget in enumerate(plot_widgets):
                if widget is not None:
                    filepath = parent / f"{stem}_graph_{i+1}{extension}"
                    if not GraphExporter.export_graph(widget, str(filepath), width, height):
                        success = False
            
            return success
        except Exception as e:
            print(f"Error exporting all graphs: {e}")
            return False
