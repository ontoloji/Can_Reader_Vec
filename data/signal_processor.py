"""
Signal Processor Module
Handles signal decoding and processing for visualization.
"""

import numpy as np
from typing import Dict, List, Any, Tuple, Optional


class SignalProcessor:
    """Class for processing and preparing CAN signals for visualization."""
    
    def __init__(self, blf_reader, dbc_parser):
        """
        Initialize the signal processor.
        
        Args:
            blf_reader: BLFReader instance
            dbc_parser: DBCParser instance
        """
        self.blf_reader = blf_reader
        self.dbc_parser = dbc_parser
        self.processed_signals: Dict[str, Dict[str, np.ndarray]] = {}
    
    def process_signal(self, message_name: str, signal_name: str) -> Optional[Tuple[np.ndarray, np.ndarray]]:
        """
        Process a specific signal from BLF data using DBC definitions.
        
        Args:
            message_name: Name of the CAN message
            signal_name: Name of the signal within the message
            
        Returns:
            Tuple of (timestamps, values) as numpy arrays, or None if processing fails
        """
        # Get message definition from DBC
        message = self.dbc_parser.get_message_by_name(message_name)
        if not message:
            print(f"Message '{message_name}' not found in DBC")
            return None
        
        # Get all messages with this ID from BLF
        blf_messages = self.blf_reader.get_messages_by_id(message.frame_id)
        if not blf_messages:
            print(f"No messages with ID {message.frame_id} found in BLF")
            return None
        
        timestamps = []
        values = []
        
        # Decode each message and extract the signal
        for msg in blf_messages:
            try:
                decoded = self.dbc_parser.decode_message(message.frame_id, msg['data'])
                if decoded and signal_name in decoded:
                    timestamps.append(msg['timestamp'])
                    values.append(decoded[signal_name])
            except Exception as e:
                # Skip messages that fail to decode
                continue
        
        if not timestamps:
            print(f"No valid data for signal '{signal_name}' in message '{message_name}'")
            return None
        
        # Convert to numpy arrays
        time_array = np.array(timestamps)
        value_array = np.array(values)
        
        # Cache the processed signal
        key = f"{message_name}.{signal_name}"
        self.processed_signals[key] = {
            'time': time_array,
            'value': value_array
        }
        
        return time_array, value_array
    
    def get_signal_info(self, message_name: str, signal_name: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a signal.
        
        Args:
            message_name: Name of the CAN message
            signal_name: Name of the signal
            
        Returns:
            Dictionary with signal information or None
        """
        message = self.dbc_parser.get_message_by_name(message_name)
        if not message:
            return None
        
        for signal in message.signals:
            if signal.name == signal_name:
                return {
                    'name': signal.name,
                    'unit': signal.unit if signal.unit else '',
                    'min': signal.minimum,
                    'max': signal.maximum,
                    'scale': signal.scale,
                    'offset': signal.offset
                }
        
        return None
    
    def get_cached_signal(self, message_name: str, signal_name: str) -> Optional[Tuple[np.ndarray, np.ndarray]]:
        """
        Get a previously processed signal from cache.
        
        Args:
            message_name: Name of the CAN message
            signal_name: Name of the signal
            
        Returns:
            Tuple of (timestamps, values) or None if not cached
        """
        key = f"{message_name}.{signal_name}"
        if key in self.processed_signals:
            data = self.processed_signals[key]
            return data['time'], data['value']
        return None
    
    def clear_cache(self):
        """Clear all cached processed signals."""
        self.processed_signals.clear()
