from dataclasses import dataclass, field
from socket import AF_INET, SOCK_STREAM, socket
from ipaddress import IPv4Address

@dataclass
class Agent:
    def connect(self, ip: IPv4Address, port: int):
        self.address = (str(ip), port)
        self.socket = socket(AF_INET, SOCK_STREAM)    
        self.socket.connect(self.address) 
        agent_port = self.socket.getsockname()[1]
        print(f"[FOXDIE: {agent_port}] connected to {port}")
        while True:
            try:
                request = input(f"[FOXDIE: {agent_port}] ")
                self.socket.send(request.encode())
                if request == "exit":
                    raise RuntimeError(f"disconnected from {port}")
                reply = self.socket.recv(1024).decode()
                print(f"[FOXDIE: {port}] {reply}")
            except RuntimeError as error:
                print(f"[FOXDIE: {agent_port}] {error}")
                break
            except KeyboardInterrupt as error:
                break
        self.socket.close()