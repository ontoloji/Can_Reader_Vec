"""
BLF Reader Module
Handles reading and parsing BLF (Binary Logging Format) files using python-can.
"""

import can
from typing import List, Dict, Any
import numpy as np


class BLFReader:
    """Class for reading BLF files and extracting CAN messages."""
    
    def __init__(self):
        self.messages: List[Dict[str, Any]] = []
        self.filepath: str = ""
        self.start_time: float = 0.0
        self.end_time: float = 0.0
        
    def load_file(self, filepath: str) -> bool:
        """
        Load and parse a BLF file.
        
        Args:
            filepath: Path to the BLF file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.filepath = filepath
            self.messages = []
            
            with can.BLFReader(filepath) as reader:
                for msg in reader:
                    self.messages.append({
                        'timestamp': msg.timestamp,
                        'arbitration_id': msg.arbitration_id,
                        'data': msg.data,
                        'dlc': msg.dlc,
                        'is_extended_id': msg.is_extended_id
                    })
            
            if self.messages:
                # Normalize timestamps to start from 0
                self.start_time = self.messages[0]['timestamp']
                self.end_time = self.messages[-1]['timestamp']
                
                for msg in self.messages:
                    msg['timestamp'] -= self.start_time
                    
                return True
            return False
            
        except Exception as e:
            print(f"Error loading BLF file: {e}")
            return False
    
    def get_messages_by_id(self, arbitration_id: int) -> List[Dict[str, Any]]:
        """
        Get all messages with a specific arbitration ID.
        
        Args:
            arbitration_id: CAN message ID
            
        Returns:
            List of messages with the specified ID
        """
        return [msg for msg in self.messages if msg['arbitration_id'] == arbitration_id]
    
    def get_unique_message_ids(self) -> List[int]:
        """
        Get list of unique message IDs in the BLF file.
        
        Returns:
            List of unique arbitration IDs
        """
        return sorted(list(set(msg['arbitration_id'] for msg in self.messages)))
    
    def get_file_info(self) -> Dict[str, Any]:
        """
        Get information about the loaded BLF file.
        
        Returns:
            Dictionary with file information
        """
        return {
            'filepath': self.filepath,
            'message_count': len(self.messages),
            'duration': self.end_time - self.start_time if self.messages else 0,
            'unique_ids': len(self.get_unique_message_ids())
        }
    def get_raw_messages(self, max_messages=None):
        """
        Get raw messages in hexadecimal format without DBC decoding.
        
        Args:
            max_messages: Maximum number of messages to return (None = all)
            
        Returns:
            List of dictionaries with timestamp, ID, and hex data
        """
        if not self.messages:
            return []
        
        raw_data = []
        count = 0
        
        for msg in self.messages:
            # Convert data to hex string
            hex_data = ' '.join([f'{byte:02X}' for byte in msg['data']])
            
            raw_data.append({
                'timestamp': msg['timestamp'],
                'id': msg['arbitration_id'],
                'id_hex': f"0x{msg['arbitration_id']:03X}",
                'dlc': len(msg['data']),
                'data_hex': hex_data
            })
            
            count += 1
            if max_messages and count >= max_messages:
                break
        
        return raw_data