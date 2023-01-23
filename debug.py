from dataclasses import dataclass, field
from ipaddress import IPv4Address
from threading import Thread
from time import sleep, time
from typing import Union
from socket import AF_INET, SOCK_STREAM, socket

time_to_stop = False

@dataclass
class Handler:
    def start(self, agent_socket: socket, agent_port: int):
        print(f"[FOXDIE: {agent_port}] connected")
        ONE_MINUTE = time() + 60
        while not time_to_stop:
            try:
                if time() > ONE_MINUTE: break
                agent_request = agent_socket.recv(1024).decode()
                if agent_request:
                    print(f"[FOXDIE: {agent_port}] {agent_request}")
                    agent_socket.send("OK".encode())
                    ONE_MINUTE = time() + 60
            except BlockingIOError: pass
            except ConnectionError: break
        print(f"[FOXDIE: {agent_port}] disconnected")

@dataclass
class Listener:
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
        while not time_to_stop:
            try:
                agent_socket, agent_address = self.socket.accept()
                agent_port = agent_address[1]
                thread = Thread(
                    name = agent_port,
                    target = self.handler.start,
                    args = [agent_socket, agent_port]
                )
                thread.start()
            except BlockingIOError: pass
        self.socket.close()
        print(f"[FOXDIE: 80] stopped listening")

@dataclass
class Server:
    listener: Listener = field(default = None, init = True)

    def start(self):
        c2 = Thread(target = self.listener)
        c2.start()
        try:
            while not time_to_stop: 
                sleep(0.5)
        except KeyboardInterrupt: 
            time_to_stop = True
            c2.join()

def main():
    listener = Listener(ip = "127.0.0.1", port = 80, handler = Handler)
    server = Server()
    server.start()

if __name__ == "__main__":
    main()