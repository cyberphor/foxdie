from dataclasses import dataclass, field
from ipaddress import IPv4Address
from threading import Event, Thread
from time import sleep, time
from socket import AF_INET, SOCK_STREAM, socket

@dataclass
class Server:
    ip: IPv4Address = field(default = "127.0.0.1") 
    port: int = field(default = 80)

    def __post_init__(self):
        self.address = (str(self.ip), self.port)
        self.done = False

    def handler(self, agent_socket: socket, agent_port: int):
        print(f"[FOXDIE: {agent_port}] connected")
        timeout = time() + 30
        while not self.done:
            try:
                if time() > timeout: break
                else:
                    agent_request = agent_socket.recv(1024).decode()
                    if agent_request:
                        print(f"[FOXDIE: {agent_port}] {agent_request}")
                        agent_socket.send("OK".encode())
                        timeout = time() + 30
            except BlockingIOError: pass
            except ConnectionError: break
        print(f"[FOXDIE: {agent_port}] disconnected")

    def dispatch(self):
        listener = socket(AF_INET, SOCK_STREAM)
        listener.bind(self.address)
        listener.listen(5)
        listener.setblocking(False)
        print(f"[FOXDIE: {self.port}] started listening")
        while not self.done:
            try:
                agent_socket, agent_address = listener.accept()
                agent_port = agent_address[1]
                thread = Thread(
                    name = agent_port,
                    target = self.handler,
                    args = [agent_socket, agent_port]
                )
                thread.start()
            except BlockingIOError: pass
        listener.close()
        print(f"[FOXDIE: {self.port}] stopped listening")

    def start(self):
        foxdie = Thread(target = self.dispatch)
        foxdie.start()
        try:
            while not self.done: sleep(0.5)
        except KeyboardInterrupt: 
            self.done = True
        foxdie.join()

def main():
    server = Server()
    server.start()

if __name__ == "__main__":
    main()