from .packet import Packet

class TokenPacket(Packet):
    
    def __init__(self) -> None:
        self.id = 1000
        
    