from dataclasses import dataclass, field
from ipaddress import IPv4Address
from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread, Event
from time import sleep, time

@dataclass
class Handler:
    killswitch: Event = field(default = None, init = True)
    agent_socket: socket = field(default = None, init = True)
    agent_port: int = field(default = None, init = True)
    def __post_init__(self):
        print(f"[FOXDIE: {self.agent_port}] connected")
        ONE_MINUTE = time() + 60
        while not self.killswitch.is_set():
            try:
                if time() > ONE_MINUTE: break
                agent_request = self.agent_socket.recv(1024).decode()
                if agent_request:
                    print(f"[FOXDIE: {self.agent_port}] {agent_request}")
                    self.agent_socket.send("OK".encode())
                    ONE_MINUTE = time() + 60
            except BlockingIOError: pass
            except ConnectionError: break
        print(f"[FOXDIE: {self.agent_port}] disconnected")

@dataclass
class Listener:
    killswitch: Event = field(default = None, init = True)
    ip: IPv4Address = field(default = None, init = True)
    port: int = field(default = None, init = True)
    handler: Handler = field(default = None, init = True)
    def start(self):
        self.address = (str(self.ip), self.port)
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind(self.address)
        self.socket.listen(5)
        self.socket.setblocking(False)
        print(f"[FOXDIE: 80] started listening")
        while not self.killswitch.is_set():
            try:
                agent_socket, agent_address = self.socket.accept()
                agent_port = agent_address[1]
                thread = Thread(
                    name = agent_port,
                    target = self.handler,
                    args = [self.killswitch, agent_socket, agent_port]
                )
                thread.start()
            except BlockingIOError: pass
        self.socket.close()
        print(f"[FOXDIE: 80] stopped listening")

@dataclass
class Server:
    killswitch: Event = field(default = None, init = True)
    listener: Listener = field(default = None, init = True)
    def start(self):
        try:
            c2 = Thread(target = self.listener.start)
            c2.start()
            while not self.killswitch.is_set(): 
                sleep(0.5)
        except KeyboardInterrupt: 
            self.killswitch.set()
        c2.join()