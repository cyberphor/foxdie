from enum import auto, Enum

class FOXDIEProtocol(Enum):
    DNS = auto()
    HTTP = auto()
    IRC = auto()
    SMB = auto()