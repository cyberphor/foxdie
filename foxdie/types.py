from enum import auto, Enum

class Protocol(Enum):
    DNS = auto()
    HTTP = auto()
    IRC = auto()
    SMB = auto()