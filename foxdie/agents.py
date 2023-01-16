from dataclasses import dataclass, field
from socket import AF_INET, SOCK_STREAM, socket
from ipaddress import IPv4Address

@dataclass
class Agent:
    address: IPv4Address = field(default = "127.0.0.1")
    port: int = field(default = 80) 

    def __post_init__(self):
        self.plug = (self.address, self.port)
        self.network = socket(AF_INET, SOCK_STREAM)

    def connect(self):
        self.network.connect(self.plug) 
        message = input("Send: ")
        while True:
            try: 
                self.network.send(message.encode())
                data = self.network.recv(1024).decode()
                if data.lower() == "exit":
                    raise Exception("Listener disconnected")
                else:
                    print(f"Recieved: {data}")
                    message = input("Send: ")
            except:
                self.network.close()
                return False