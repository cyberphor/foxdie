from dataclasses import dataclass, field
from ipaddress import IPv4Address
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Thread, current_thread
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
        agent_thread = current_thread()
        while True:
            if agent_thread.is_alive:
                agent_request = agent_connection.recv(1024).decode()
                print(f"[FOXDIE: {agent_port}] {agent_request}")
                server_reply = "OK"
                agent_connection.send(server_reply.encode())
                print(f"[FOXDIE: {self.port}] {server_reply}")
            else:
                agent_thread.join(0.5)
                break
        agent_connection.close()

    def listen(self):
        """
        TODO: add logic outside this function to
        - monitor for exceptions raised (i.e., keyboard) interrupt 
        - start threads
        - if interrupted, 
          - kill all threads
        """
        listener = socket(AF_INET, SOCK_STREAM)
        listener.bind(self.address)
        listener.listen(5)
        print(f"[FOXDIE: {self.port}] is listening")
        while True:
            try:
                agent_socket, agent_address = listener.accept()
                agent_port = agent_address[1]
                print(f"[FOXDIE: {self.port}] connected from {agent_port}")
                agent_thread = Thread(
                    name = agent_port, 
                    target = self.handle, 
                    args = (agent_socket, agent_port)
                )
                agent_thread.start()
                self.threads.append(agent_thread)
            except KeyboardInterrupt as error:
                for thread in self.threads:
                    thread.alive = False
                    thread.join()
                break
        listener.close()
        print(f"[FOXDIE: {self.port}] stopped listening")