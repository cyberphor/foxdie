from dataclasses import dataclass, field
from ipaddress import IPv4Address
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Thread
from typing import List

@dataclass
class Server:
    ip: IPv4Address = field(default = None)
    port: int = field(default = None)
    threads: list[Thread] = field(default_factory = list, init = None)

    def __post_init__(self):
        self.address = (str(self.ip), self.port)
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind(self.address)
        self.socket.listen(5)
        self.socket.settimeout(60)

    def handle(self, agent_connection, agent_port):
        agent_request = agent_connection.recv(1024).decode()
        print(f"[FOXDIE: {agent_port}] {agent_request}")
        server_reply = "Thanks bye!".encode()
        agent_connection.send(server_reply)
        agent_connection.close()

    def listen(self):
        print(f"[FOXDIE: {self.port}] Listening.")
        while True:
            try:
                agent_socket, agent_address = self.socket.accept()
                agent_port = agent_address[1]
                thread = Thread(
                    name = agent_port, 
                    target = self.handle, 
                    args = (agent_socket, agent_port)
                )
                thread.start()
                self.threads.append(thread)
                print(f"[FOXDIE: {agent_port}] Connected.")
            except TimeoutError as e:
                print(f"[FOXDIE: {self.port}] {e}")
                break
            except KeyboardInterrupt:
                break
        self.socket.close()
        print(f"[FOXDIE: {self.port}] Stopped listening.")