import socket
from .packet import Packet
from typing import Optional
from .message_queue import MessageQueue

class NetworkNode:
    
    def __init__(self,
                 IP: str,
                 nickname: str,
                 right_neighbor: Optional[str],
                 has_token: bool = False) -> None:
        
        self.IP = IP
        self.nickname = nickname
        self.right_neighbor = right_neighbor
        self.has_token = has_token
        self.message_queue = MessageQueue()
        
        
    def send_message(self, target: str, content: Packet):
        
        if self.has_token:
            return True
        else:
            return False