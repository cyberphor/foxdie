from dataclasses import dataclass, field
from ipaddress import IPv4Address
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

@dataclass
class Listener:
    address: IPv4Address = field(default = "127.0.0.1")
    port: int = field(default = 80) 

    def __post_init__(self):
        self.plug = (self.address, self.port)
        self.network = socket(AF_INET, SOCK_STREAM)
        self.network.bind(self.plug) 
        self.network.listen(2)
        self.threads = []
        print(f"[{self.address}] Listening for connections.")

    def start(self):
        while True:
            agent_socket, agent_address = self.network.accept()
            agent_socket.settimeout(60)
            thread = Thread(
                name = agent_address[1], 
                target = self.handle, 
                args = (agent_socket, agent_address)
            )
            thread.start()
            print(f"[{agent_address[0]}] Connected (thread: {thread.name}).")
            self.threads.append(thread)

    def handle(self, agent_socket, agent_address):
        while True:
            try:
                data = agent_socket.recv(1024)
                if data:
                    print(f"[{agent_address[0]}] {data.decode()}")
                    response = data
                    agent_socket.send(response)
                else:
                    raise Exception("Agent disconnected")
            except:
                agent_socket.close()
                return False