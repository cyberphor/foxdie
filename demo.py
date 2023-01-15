from foxdie.server import FOXDIEServer
from foxdie.handlers import FOXDIEHandler
from foxdie.types import FOXDIEProtocol

h = FOXDIEHandler(
    protocol = FOXDIEProtocol.DNS
) 

h.start()