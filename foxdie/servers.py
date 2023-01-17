from dataclasses import dataclass, field
from ipaddress import IPv4Address
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from typing import List

@dataclass
class Server:
    address: IPv4Address = field(default = None)
    port: int = field(default = None)
    threads: List[Thread] = field(default_factory = list, init = False)

    def __post_init__(self):
        self.plug = (str(self.address), self.port)
            
    def start(self):
        def stop(self):
            self.socket.close()
            print(f"[FOXDIE: {self.port}] Stopped listening.")
            for thread in self.threads:
                thread.join()
                print(f"[FOXDIE: {thread.name}] Disconnected.")
            return False

        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind(self.plug) 
        self.socket.listen(2)
        print(f"[FOXDIE: {self.port}] Listening.")
        try:
            while True:
                agent_connection, agent_plug = self.socket.accept()
                agent_port = agent_plug[1]
                agent_connection.settimeout(60)
                thread = Thread(
                    name = agent_port, 
                    target = self.handle, 
                    args = (agent_connection, agent_port)
                )
                thread.start()
                self.threads.append(thread)
                print(f"[FOXDIE: {thread.name}] Connected.")
        except:
            stop()

    def handle(self, agent_connection, agent_port):
        try:
            data = agent_connection.recv(1024).decode()
            if data.lower() == "exit":
                raise Exception(f"[FOXDIE: {agent_port}] Disconnected.")
            else:
                print(f"[FOXDIE: {agent_port}] {data}")
                response = input(f"[FOXDIE: {self.port}] ")
                agent_connection.send(response.encode())
        except:
            agent_connection.close()
            self.threads[agent_port].join
            return False