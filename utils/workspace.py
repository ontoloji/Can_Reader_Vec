"""
Workspace Module
Handles saving and loading workspace configurations.
"""

import json
from typing import Dict, Any, Optional
from pathlib import Path


class Workspace:
    """Class for managing workspace save/load operations."""
    
    @staticmethod
    def save(filepath: str, workspace_data: Dict[str, Any]) -> bool:
        """
        Save workspace configuration to a JSON file.
        
        Args:
            filepath: Path to save the workspace file
            workspace_data: Dictionary containing workspace configuration
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(filepath, 'w') as f:
                json.dump(workspace_data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving workspace: {e}")
            return False
    
    @staticmethod
    def load(filepath: str) -> Optional[Dict[str, Any]]:
        """
        Load workspace configuration from a JSON file.
        
        Args:
            filepath: Path to the workspace file
            
        Returns:
            Dictionary containing workspace configuration or None if failed
        """
        try:
            if not Path(filepath).exists():
                print(f"Workspace file not found: {filepath}")
                return None
            
            with open(filepath, 'r') as f:
                workspace_data = json.load(f)
            
            return workspace_data
        except Exception as e:
            print(f"Error loading workspace: {e}")
            return None
    
    @staticmethod
    def create_workspace_data(
        blf_path: str,
        dbc_path: str,
        selected_signals: list,
        view_range: Dict[str, float],
        window_geometry: Dict[str, int]
    ) -> Dict[str, Any]:
        """
        Create a workspace data dictionary.
        
        Args:
            blf_path: Path to BLF file
            dbc_path: Path to DBC file
            selected_signals: List of selected signals
            view_range: Dictionary with x_min and x_max
            window_geometry: Dictionary with width and height
            
        Returns:
            Workspace data dictionary
        """
        return {
            'blf_path': blf_path,
            'dbc_path': dbc_path,
            'selected_signals': selected_signals,
            'view_range': view_range,
            'window_geometry': window_geometry
        }
