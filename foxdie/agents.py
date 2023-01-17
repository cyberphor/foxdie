from dataclasses import dataclass, field
from socket import AF_INET, SOCK_STREAM, socket
from ipaddress import IPv4Address

@dataclass
class Agent:
    def connect(self, address: IPv4Address, port: int):
        self.plug = (str(address), port)
        self.socket = socket(AF_INET, SOCK_STREAM)    
        self.socket.connect(self.plug) 
        message = input(f"[FOXDIE: {self.socket.getsockname()[1]}] ")
        while True:
            try: 
                self.socket.send(message.encode())
                data = self.socket.recv(1024).decode()
                if data.lower() == "exit":
                    raise Exception(f"[FOXDIE: {port}] Disconnected.")
                else:
                    print(f"[FOXDIE: {port}] {data}")
                    message = input(f"[FOXDIE: {self.socket.getsockname()[1]}] ")
            except:
                self.socket.close()
                return False