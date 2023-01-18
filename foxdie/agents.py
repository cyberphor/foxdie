from dataclasses import dataclass, field
from socket import AF_INET, SOCK_STREAM, socket
from ipaddress import IPv4Address

@dataclass
class Agent:
    def connect(self, ip: IPv4Address, port: int):
        self.address = (str(ip), port)
        self.socket = socket(AF_INET, SOCK_STREAM)    
        self.socket.connect(self.address) 
        while True:
            try: 
                message = input(f"[FOXDIE: {self.socket.getsockname()[1]}] ")
                self.socket.send(message.encode())
                reply = self.socket.recv(1024).decode()
                if reply:
                    print(f"[FOXDIE: {port}] {reply}")
                else:
                    break
            except:
                break
        self.socket.close()