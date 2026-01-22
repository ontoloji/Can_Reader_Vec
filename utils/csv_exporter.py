"""
CSV Exporter Module
Exports signal data to CSV format.
"""

import csv
import numpy as np
from typing import Dict, Optional, Tuple


class CSVExporter:
    """Exporter for signal data to CSV format."""
    
    @staticmethod
    def export_signals(filename: str, signal_data_dict: Dict[str, Dict],
                      time_range: Optional[Tuple[float, float]] = None) -> bool:
        """
        Export signal data to CSV file.
        
        Args:
            filename: Path to save CSV file
            signal_data_dict: Dictionary with signal data
                Format: {
                    'signal_key': {
                        'time': np.ndarray,
                        'value': np.ndarray,
                        'unit': str,
                        'message': str,
                        'signal': str
                    }
                }
            time_range: Optional tuple (start_time, end_time) to export only a range
            
        Returns:
            True if export successful, False otherwise
        """
        try:
            if not signal_data_dict:
                print("No signal data to export")
                return False
            
            # Collect all data and find common time base
            signal_arrays = {}
            all_times = []
            
            for signal_key, data in signal_data_dict.items():
                if data is None or 'time' not in data or 'value' not in data:
                    continue
                
                time_array = data['time']
                value_array = data['value']
                
                # Apply time range filter if specified
                if time_range:
                    t_start, t_end = time_range
                    mask = (time_array >= t_start) & (time_array <= t_end)
                    time_array = time_array[mask]
                    value_array = value_array[mask]
                
                if len(time_array) == 0:
                    continue
                
                signal_arrays[signal_key] = {
                    'time': time_array,
                    'value': value_array,
                    'unit': data.get('unit', ''),
                    'message': data.get('message', ''),
                    'signal': data.get('signal', signal_key)
                }
                all_times.extend(time_array.tolist())
            
            if not signal_arrays:
                print("No valid signal data after filtering")
                return False
            
            # Create unified time base (merge all time stamps)
            unified_time = np.unique(np.sort(np.array(all_times)))
            
            # Interpolate all signals to unified time base
            interpolated_data = {}
            for signal_key, data in signal_arrays.items():
                # Use linear interpolation for intermediate values
                interpolated_values = np.interp(
                    unified_time,
                    data['time'],
                    data['value']
                )
                interpolated_data[signal_key] = {
                    'values': interpolated_values,
                    'unit': data['unit'],
                    'message': data['message'],
                    'signal': data['signal']
                }
            
            # Write CSV file
            with open(filename, 'w', newline='') as csvfile:
                # Create header
                header = ['Time (s)']
                for signal_key, data in interpolated_data.items():
                    signal_name = data['signal']
                    message_name = data['message']
                    unit = data['unit']
                    
                    # Format column name
                    if message_name:
                        col_name = f"{message_name}.{signal_name}"
                    else:
                        col_name = signal_name
                    
                    if unit:
                        col_name += f" ({unit})"
                    
                    header.append(col_name)
                
                writer = csv.writer(csvfile)
                writer.writerow(header)
                
                # Write data rows
                for i, time_val in enumerate(unified_time):
                    row = [f"{time_val:.6f}"]
                    for signal_key in interpolated_data.keys():
                        value = interpolated_data[signal_key]['values'][i]
                        row.append(f"{value:.6f}")
                    writer.writerow(row)
            
            return True
            
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return False
