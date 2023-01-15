from dataclasses import dataclass, field
from socket import AF_INET, SOCK_STREAM, socket
from ipaddress import IPv4Address

@dataclass
class Listener:
    """Listener"""
    address: IPv4Address = field(default = "127.0.0.1")
    port: int = field(default = 80)

    def __post_init__(self):
        plug = (self.address, self.port)
        listener = socket(AF_INET, SOCK_STREAM)
        listener.bind(plug)

@dataclass
class Handler():
    listeners: list[Listener]

    def start():
        """Start handler."""
        print("Started listener")

    def stop():
        """Stop handler."""
        print("Stopped listener")

    def start_listener(self):
        """Start listener."""
        print("Started listener")

    def stop_listener(self):
        """Stop listener."""
        print("Stopped listener")