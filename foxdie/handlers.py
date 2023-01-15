from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from foxdie.types import FOXDIEProtocol

@dataclass
class FOXDIEHandler(ABC):
    protocol: FOXDIEProtocol

    def __post_init__(self):
        self.protocol = FOXDIEProtocol[self.protocol.name].name

    @abstractmethod
    def start(self):
        print(self.protocol)

@dataclass
class Foo(FOXDIEHandler):
    def start(self):
        super().start() # return a 'start' func to parent class
        print("Protocol: " + self.protocol)