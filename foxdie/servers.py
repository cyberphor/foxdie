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

    def handle(self, agent_connection, agent_port):
        while True:
            agent_request = agent_connection.recv(1024).decode()
            print(f"[FOXDIE: {agent_port}] {agent_request}")
            if agent_request == "exit":
                break
            server_reply = "Thanks bye!"
            print(f"[FOXDIE: {self.port}] {server_reply}")
            agent_connection.send(server_reply.encode())
        print(f"[FOXDIE: {agent_port}] disconnected")
        agent_connection.close()

    def listen(self):
        s = socket(AF_INET, SOCK_STREAM)
        s.bind(self.address)
        s.listen(5)
        s.settimeout(120)
        print(f"[FOXDIE: {self.port}] listening")
        while True:
            try:
                agent_socket, agent_address = s.accept()
                agent_port = agent_address[1]
                print(f"[FOXDIE: {agent_port}] connected")
                thread = Thread(
                    name = agent_port, 
                    target = self.handle, 
                    args = (agent_socket, agent_port)
                )
                thread.start()
                self.threads.append(thread)
            except :
                print(f"[FOXDIE: {self.port}] error")
                break
        s.close()
        print(f"[FOXDIE: {self.port}] stopped listening")