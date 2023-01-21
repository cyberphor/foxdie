from dataclasses import dataclass, field
from ipaddress import IPv4Address
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Thread, current_thread
from typing import List

@dataclass
class Handler:
    """Handler"""
    agent_connection: socket
    agent_port: int
    agent_thread = current_thread()
    while agent_thread.is_alive:
        agent_request = agent_connection.recv(1024).decode()
        if agent_request:
            print(f"[FOXDIE: {agent_port}] {agent_request}")
            server_reply = "OK"
            agent_connection.send(server_reply.encode())
    agent_connection.close()

@dataclass
class Listener(socket):
    """Listener"""
    ip: IPv4Address
    port: int

    def __post_init__(self):
        self.address = (str(self.ip), self.port)
        self.bind(self.address)
        self.listen(5)
        self.setblocking(False)
        print(f"[FOXDIE: {self.port}] is listening")
        while True:
            try:
                agent_socket, agent_address = self.accept()
                agent_port = agent_address[1]
                print(f"[FOXDIE: {self.port}] connected from {agent_port}")
                agent_thread = Thread(
                    name = agent_port, 
                    target = self.handler, 
                    args = (agent_socket, agent_port)
                )
                agent_thread.start()
                self.threads.append(agent_thread)
            except BlockingIOError as e:
                pass
            except KeyboardInterrupt:
                for thread in self.threads:
                    thread.alive = False
                    thread.join()
                break
        self.close()
        print(f"[FOXDIE: {self.port}] stopped listening")

@dataclass
class Server:
    ip: IPv4Address = field(default = None)
    port: int = field(default = None)
    threads: list[Thread] = field(default_factory = list, init = None)

    def __post_init__(self):
        self.address = (str(self.ip), self.port)
        self.listener = Listener(self.address)