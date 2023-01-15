from dataclasses import dataclass, field
from foxdie.handlers import FOXDIEHandler

@dataclass
class FOXDIEServer:
    name: str = field(default = None)

    def start_handler(self, h: FOXDIEHandler):
        h.start()
