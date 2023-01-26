from dataclasses import dataclass, field
from ipaddress import IPv4Address
from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread, Event
from typing import Dict
from time import sleep, time

@dataclass
class Handler:
    def start(self, agent_socket: socket, agent_port: int, killswitch: Event):
        print(f"[FOXDIE: {self.agent_port}] connected")
        ONE_MINUTE = time() + 60
        while not killswitch.is_set():
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
    ip: IPv4Address
    port: int 

    def __key(self):
        return (self.ip, self.port)

    def __hash__(self):
        return hash(self.__key())
        
    def __eq__(self, other):
        if isinstance(other, Listener):
            return self.__key() == other.__key()
        return NotImplemented

    def start(self, handler: Handler, killswitch: Event):
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
                    target = handler.start,
                    args = [self.killswitch, agent_socket, agent_port]
                )
                thread.start()
            except BlockingIOError: pass
        self.socket.close()
        print(f"[FOXDIE: 80] stopped listening")

@dataclass
class Server:
    workers: Dict[Listener, Handler]
    killswitch: Event = field(default_factory = Event)

    def foo(self):
        for foo in self.workers.items():
            print(dir(foo))

    def bar(self):
        print(self.workers[Listener(ip = "127.0.0.1", port = 80)])
        
    def start(self):
        try:
            thread = Thread(
                target = self.listener.start,
                args = [self.killswitch]
            )
            thread.start()
            while not self.killswitch.is_set(): 
                sleep(0.5)
        except KeyboardInterrupt: 
            self.killswitch.set()
            thread.join()

