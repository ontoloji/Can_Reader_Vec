"""
Partial Data Exporter Module
Exports and imports partial signal data in JSON format.
"""

import json
import numpy as np
from typing import Dict, Tuple, Optional
from datetime import datetime


class PartialDataExporter:
    """Exporter for partial signal data to JSON format."""
    
    @staticmethod
    def export_time_range(filename: str, signal_data_dict: Dict[str, Dict],
                         time_range: Tuple[float, float], 
                         metadata: Optional[Dict] = None) -> bool:
        """
        Export signal data for a specific time range to JSON.
        
        Args:
            filename: Path to save JSON file
            signal_data_dict: Dictionary with signal data
            time_range: Tuple (start_time, end_time)
            metadata: Optional metadata to include in export
            
        Returns:
            True if export successful, False otherwise
        """
        try:
            t_start, t_end = time_range
            
            # Build metadata
            if metadata is None:
                metadata = {}
            
            metadata.update({
                'export_date': datetime.now().isoformat(),
                'app_name': 'CAN Data Viewer',
                'app_version': '1.1.0'
            })
            
            # Build export data structure
            export_data = {
                'metadata': metadata,
                'time_range': {
                    'start': float(t_start),
                    'end': float(t_end),
                    'duration': float(t_end - t_start)
                },
                'signals': {}
            }
            
            # Process each signal
            for signal_key, data in signal_data_dict.items():
                if data is None or 'time' not in data or 'value' not in data:
                    continue
                
                time_array = data['time']
                value_array = data['value']
                
                # Filter by time range
                mask = (time_array >= t_start) & (time_array <= t_end)
                filtered_time = time_array[mask]
                filtered_value = value_array[mask]
                
                if len(filtered_time) == 0:
                    continue
                
                # Store signal data
                signal_name = data.get('signal', signal_key)
                message_name = data.get('message', '')
                
                if message_name:
                    full_key = f"{message_name}.{signal_name}"
                else:
                    full_key = signal_name
                
                export_data['signals'][full_key] = {
                    'message': message_name,
                    'signal': signal_name,
                    'unit': data.get('unit', ''),
                    'time': filtered_time.tolist(),
                    'value': filtered_value.tolist(),
                    'sample_count': len(filtered_time)
                }
            
            # Write to JSON file
            with open(filename, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            return True
            
        except Exception as e:
            print(f"Error exporting partial data: {e}")
            return False
    
    @staticmethod
    def load_partial_data(filename: str) -> Optional[Dict]:
        """
        Load partial data from JSON file.
        
        Args:
            filename: Path to JSON file
            
        Returns:
            Dictionary with loaded data or None if failed
        """
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            # Convert lists back to numpy arrays
            for signal_key in data.get('signals', {}):
                signal_data = data['signals'][signal_key]
                signal_data['time'] = np.array(signal_data['time'])
                signal_data['value'] = np.array(signal_data['value'])
            
            return data
            
        except Exception as e:
            print(f"Error loading partial data: {e}")
            return None
    
    @staticmethod
    def get_data_summary(filename: str) -> Optional[Dict]:
        """
        Get summary information about a partial data file without loading full data.
        
        Args:
            filename: Path to JSON file
            
        Returns:
            Dictionary with summary info or None if failed
        """
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            summary = {
                'metadata': data.get('metadata', {}),
                'time_range': data.get('time_range', {}),
                'signal_count': len(data.get('signals', {})),
                'signal_names': list(data.get('signals', {}).keys())
            }
            
            return summary
            
        except Exception as e:
            print(f"Error reading data summary: {e}")
            return None
