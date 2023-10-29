from abc import ABC, abstractmethod

class Packet(ABC):
    
    def __init__(self, id: str) -> None:
        self.id = id
        
    