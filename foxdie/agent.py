from dataclasses import dataclass
from foxdie.payloads import payloads
from ipaddress import IPv4Address
from socket import AF_INET, SOCK_STREAM, socket

@dataclass
class Agent:
    server_ip: IPv4Address
    server_port: int 
    request: str

    def __post_init__(self):
        self.address = (str(self.server_ip), self.server_port)
        self.socket = socket(AF_INET, SOCK_STREAM)

    def execute(self, reply):
        print(f"{reply}")

    def start(self):
        self.socket.connect(self.address) 
        self.socket.send(self.request.encode())
        self.execute(self.socket.recv(1024).decode())
        self.socket.close()