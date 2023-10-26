import json
import zlib

class Packet:
    
    def __init__(self, content: str, packet_type: str) -> None:
        self.content = content 
        self.packet_type = packet_type
        self.crc32 = self.calculate_crc32()
        
        
    def calculate_crc32(self):
        return zlib.crc32(self.content.encode())
    
    
    def is_valid(self, received_crc32: int) -> bool:
        return self.crc32 == received_crc32


    def to_bytes(self) -> bytes:
        packet_dict = {
            "content": self.content,
            "packet_type": self.packet_type,
            "crc32": self.crc32
        }
        
        return json.dumps(packet_dict).encode()
    
    @staticmethod
    def from_bytes(data: bytes) -> "Packet":
        
        packet_dict = json.loads(data.decode())
        packet = Packet(packet_dict["content"], packet_dict["packet_type"])
        packet.crc32 = packet_dict["crc32"]
        return packet