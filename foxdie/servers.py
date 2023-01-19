from dataclasses import dataclass, field
from ipaddress import IPv4Address
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Thread
from typing import List

@dataclass
class Handler:
    """Handler"""

@dataclass
class Listener:
    """Listener"""

@dataclass
class Server:
    ip: IPv4Address = field(default = None)
    port: int = field(default = None)
    threads: list[Thread] = field(default_factory = list, init = None)

    def __post_init__(self):
        self.address = (str(self.ip), self.port)

    def handle(self, agent_connection, agent_port):
        while True:
            try:
                agent_request = agent_connection.recv(1024).decode()
                print(f"[FOXDIE: {agent_port}] {agent_request}")
                server_reply = "OK"
                agent_connection.send(server_reply.encode())
                print(f"[FOXDIE: {self.port}] {server_reply}")
            except Exception as error:
                print(f"[FOXDIE: {agent_port}] {error}")
                break 
        agent_connection.close()

    def listen(self):
        listener = socket(AF_INET, SOCK_STREAM)
        listener.bind(self.address)
        listener.listen(5)
        listener.setblocking(False)
        print(f"[FOXDIE: {self.port}] listening")
        while True:
            try:
                try:
                    agent_socket, agent_address = listener.accept()
                    agent_port = agent_address[1]
                    print(f"[FOXDIE: {self.port}] connected from {agent_port}")
                    thread = Thread(
                        name = agent_port, 
                        target = self.handle, 
                        args = (agent_socket, agent_port)
                    )
                    thread.start()
                    self.threads.append(thread)
                except BlockingIOError:
                    pass
            except KeyboardInterrupt:
                break
        listener.close()
        print(f"[FOXDIE: {self.port}] stopped listening")