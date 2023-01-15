from dataclasses import dataclass, field
from socket import AF_INET, SOCK_STREAM, socket
from ipaddress import IPv4Address

@dataclass
class Agent:
    """Agent"""
    
    def connect(address: IPv4Address, port: int):
        plug = (address, port)
        listener = socket(AF_INET, SOCK_STREAM)
        listener.connect(plug)