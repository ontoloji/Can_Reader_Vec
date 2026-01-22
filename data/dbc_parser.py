"""
DBC Parser Module
Handles parsing DBC (CAN Database) files using cantools.
"""

import cantools
from typing import Dict, List, Any, Optional


class DBCParser:
    """Class for parsing DBC files and managing CAN message definitions."""
    
    def __init__(self):
        self.database: Optional[cantools.database.Database] = None
        self.filepath: str = ""
        
    def load_file(self, filepath: str) -> bool:
        """
        Load and parse a DBC file.
        
        Args:
            filepath: Path to the DBC file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.filepath = filepath
            self.database = cantools.database.load_file(filepath)
            return True
        except Exception as e:
            print(f"Error loading DBC file: {e}")
            return False
    
    def get_messages(self) -> List[Dict[str, Any]]:
        """
        Get all messages defined in the DBC file.
        
        Returns:
            List of message information dictionaries
        """
        if not self.database:
            return []
        
        messages = []
        for msg in self.database.messages:
            messages.append({
                'name': msg.name,
                'id': msg.frame_id,
                'dlc': msg.length,
                'signals': [
                    {
                        'name': sig.name,
                        'unit': sig.unit if sig.unit else '',
                        'min': sig.minimum if sig.minimum is not None else 0,
                        'max': sig.maximum if sig.maximum is not None else 0,
                        'scale': sig.scale,
                        'offset': sig.offset
                    }
                    for sig in msg.signals
                ]
            })
        
        return messages
    
    def get_message_by_id(self, message_id: int) -> Optional[Any]:
        """
        Get a message definition by its ID.
        
        Args:
            message_id: CAN message ID
            
        Returns:
            Message object or None if not found
        """
        if not self.database:
            return None
        
        try:
            return self.database.get_message_by_frame_id(message_id)
        except KeyError:
            return None
    
    def get_message_by_name(self, message_name: str) -> Optional[Any]:
        """
        Get a message definition by its name.
        
        Args:
            message_name: Name of the message
            
        Returns:
            Message object or None if not found
        """
        if not self.database:
            return None
        
        try:
            return self.database.get_message_by_name(message_name)
        except KeyError:
            return None
    
    def decode_message(self, message_id: int, data: bytes) -> Optional[Dict[str, Any]]:
        """
        Decode a CAN message using the DBC definition.
        
        Args:
            message_id: CAN message ID
            data: Raw message data bytes
            
        Returns:
            Dictionary of decoded signals or None if decoding fails
        """
        message = self.get_message_by_id(message_id)
        if not message:
            return None
        
        try:
            return message.decode(data)
        except Exception as e:
            print(f"Error decoding message {message_id}: {e}")
            return None
    
    def get_file_info(self) -> Dict[str, Any]:
        """
        Get information about the loaded DBC file.
        
        Returns:
            Dictionary with file information
        """
        if not self.database:
            return {
                'filepath': '',
                'message_count': 0,
                'signal_count': 0
            }
        
        signal_count = sum(len(msg.signals) for msg in self.database.messages)
        
        return {
            'filepath': self.filepath,
            'message_count': len(self.database.messages),
            'signal_count': signal_count
        }
