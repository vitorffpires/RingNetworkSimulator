from .packet import Packet

class DataPacket(Packet):
    
    def __init__(self, origin_name: str, destination_name: str, error_control: str, crc: str, message: str) -> None:
        self.id = "2000"
        self.origin_name = origin_name
        self.destination_name = destination_name 
        self.error_control = error_control,
        self.crc = crc
        self.message = message