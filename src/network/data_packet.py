from .packet import Packet

class DataPacket(Packet):
    
    def __init__(self, origin_name: str, destination_name: str, error_control : str, crc: str, message: str) -> None:
        super().__init__("2000")
        self.origin_name = origin_name
        self.destination_name = destination_name 
        self.error_control = error_control
        self.crc = crc
        self.message = message
        self.header = self.create_header()
        
    def create_header(self):
        return f"{self.id};{self.origin_name};{self.destination_name};{self.error_control};{self.crc};{self.message}"
    
    def calculate_crc(self, message: str):
        # TODO implement the method
        pass

    def aux_create_packet(self, origin_name: str, destination_name: str, message: str):
        return DataPacket(origin_name, destination_name, "maquinanaoexiste", self.calculate_crc(message), message)

    @classmethod
    def create_header_from_string(cls, header: str):
        header = header.split(";")
        return DataPacket(header[1], header[2], header[3], header[4], header[5])
