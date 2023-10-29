class Machine:
    
    def __init__(self, ip: str, nickname: str, time_token: str, has_token: bool = False) -> None:
        self.ip = ip
        self.nickname = nickname
        self.time_token = time_token
        self.has_token = has_token
        self.message_queue = []
        