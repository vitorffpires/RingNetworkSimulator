import socket
from .packet import Packet
from .data_packet import DataPacket
from .token_packet import TokenPacket

class Machine:
    
    def __init__(self, ip: str, nickname: str, time_token: str, has_token: bool = False) -> None:
        self.ip = Machine.get_ip(ip)
        self.port = int(Machine.get_port(ip))
        self.nickname = nickname
        self.time_token = time_token
        self.has_token = has_token
        self.message_queue = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        if self.has_token == True:
            self.generate_token()
        
    def generate_token(self):
        self.token = TokenPacket()
        
    def add_packet_to_queue(self, packet: Packet):
        self.message_queue.append(packet)

    def get_packet_from_queue(self):
        if self.has_token:
            return self.message_queue.pop(0)
        else:
            return None

    def insert_error(self):
        # TODO implement the class to insert sintetic errors
        pass 

    def send_packet(self, packet: Packet):
        self.socket.sendto(packet.header.encode(), (self.ip, self.port))
        
    def receive_packet(self):
        data, addr = self.socket.recvfrom(1024)  # buffer size is 1024 bytes
        type = Packet.get_packet_type(data.decode())
        if type == "1000":
            packet = TokenPacket()
        elif type == "2000":
            packet = DataPacket.create_header_from_string(data.decode())
            
        return self.process_packet(packet)
    
    def configure_machine(file_path: str) -> 'Machine':
        with open(file_path, 'r') as f:
            ip_port = f.readline().strip()
            nickname = f.readline().strip()
            time_token = f.readline().strip()
            token = bool(f.readline().strip())

        machine = Machine(ip_port, nickname, time_token, token)
        return machine

    @classmethod
    def get_ip(cls, ip: str):
        return ip.split(":")[0]
    
    @classmethod
    def get_port(cls, ip: str):
        return ip.split(":")[1]
    
    def close_socket(self):
        self.socket.close()
        
    def process_packet(self, packet: Packet):
        if packet.id == "1000":
            self.has_token = True
            message = self.get_packet_from_queue()
            if message is not None:
                self.send_packet(message)
            else:
                self.send_packet(TokenPacket())
        elif packet.id == "2000":
            if packet.destination_name == self.nickname:
                crc = packet.calculate_crc(packet.message)
                if crc == packet.crc:
                    print(f"Message from {packet.origin_name}: {packet.message}")
                    packet.error_control = 'ACK'
                else:
                    print(f"Message from {packet.origin_name} with error: original crc: {packet.crc}, calculated crc: {crc}")
                self.send_packet(packet=packet)
            elif packet.origin_name == self.nickname:
                if packet.error_control == "maquinanaoexiste":
                    self.message_queue.remove(packet)
                    self.send_packet(packet=Packet('1000'))
                    print('Error: Machine does not exist')
                if packet.error_control == "NAK":
                    self.send_packet(packet=Packet('1000'))
                    print('Error: The target machine identified a CRC error')
                if packet.error_control == "ACK":
                    self.message_queue.remove(packet)
                    self.send_packet(packet=Packet('1000'))
                    print('Message sent successfully')
            else:
                self.send_packet(packet)