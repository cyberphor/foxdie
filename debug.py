from dataclasses import dataclass, field
from ipaddress import IPv4Address
from threading import Event, Thread
from time import sleep
from socket import socket, AF_INET, SOCK_STREAM

@dataclass
class Server:
    ip: IPv4Address = field(default = "127.0.0.1") 
    port: int = field(default = 80)

    def __post_init__(self):
        self.sun = Event()
        self.address = (str(self.ip), self.port)

    def handler(self, agent_socket: socket, agent_port: int):
        print(f"[FOXDIE: {agent_port}] connected")
        while not self.sun.is_set():
            # TODO: set timer to close socket if not data is recv in 60 seconds
            try:
                agent_request = agent_socket.recv(1024).decode()
                if agent_request:
                    print(f"[FOXDIE: {agent_port}] {agent_request}")
                    agent_socket.send("OK".encode())
            except BlockingIOError:
                pass
            except ConnectionError:
                break
        print(f"[FOXDIE: {agent_port}] disconnected")

    def dispatch(self):
        listener = socket(AF_INET, SOCK_STREAM)
        listener.bind(self.address)
        listener.listen(5)
        listener.setblocking(False)
        print(f"[FOXDIE: {self.port}] started listening")
        while not self.sun.is_set():
            try:
                agent_socket, agent_address = listener.accept()
                agent_port = agent_address[1]
                thread = Thread(
                    name = agent_port,
                    target = self.handler,
                    args = [agent_socket, agent_port]
                )
                thread.start()
            except BlockingIOError:
                pass
        listener.close()
        print(f"[FOXDIE: {self.port}] stopped listening")

    def start(self):
        foxdie = Thread(target = self.dispatch)
        foxdie.start()
        try:
            while not self.sun.is_set():
                sleep(0.5)
        except KeyboardInterrupt:
            self.sun.set()
        foxdie.join()

def main():
    server = Server()
    server.start()

if __name__ == "__main__":
    main()