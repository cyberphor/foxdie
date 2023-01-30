from dataclasses import dataclass, field
from foxdie.payloads import payloads
from ipaddress import IPv4Address
from socket import AF_INET, SOCK_STREAM, socket
from threading import Thread, Event

@dataclass
class Server:
    ip: IPv4Address
    port: int
    killswitch: Event = field(default_factory = Event)

    def __post_init__(self):
        self.address = (str(self.ip), self.port)
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind(self.address)
        self.socket.listen(5)
        self.socket.setblocking(False)

    def handler(self, agent: socket):
        server_ip, server_port = agent.getsockname()
        agent_ip, agent_port = agent.getpeername()
        request = agent.recv(1024).decode()
        print(f"{server_ip} {server_port} < {agent_port} {agent_ip} {request}")
        reply = payloads[request]
        agent.send(reply.encode())
        print(f"{server_ip} {server_port} > {agent_port} {agent_ip} {reply}")
        agent.close()

    def dispatch(self):
        while not self.killswitch.is_set():
            try:
                agent, _ = self.socket.accept()
                thread = Thread(target = self.handler, args = [agent])
                thread.start()
            except BlockingIOError: 
                pass

    def start(self):
        print(f"[FOXDIE] started listening")
        try:
            self.dispatch()
        except KeyboardInterrupt:
            self.killswitch.set()
        print(f"[FOXDIE] stopped listening")