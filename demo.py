from argparse import ArgumentParser
from foxdie.agents import Agent
from foxdie.servers import Server, Listener, Handler
from ipaddress import IPv4Address
from threading import Event

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-m", "--mode", type = str, choices = ["server", "agent"])
    parser.add_argument("-i", "--ip-address", type = IPv4Address, required = True)
    parser.add_argument("-p", "--port", type = int, required = True)
    args = parser.parse_args()
    if args.mode == "server":
        event = Event()
        server = Server(
            killswitch = event,
            listener = Listener(
                killswitch = event,
                ip = args.ip_address, 
                port = args.port, 
                handler = Handler
            )
        )
        server.start()
    elif args.mode == "agent":
        agent = Agent()
        agent.connect(ip = args.ip_address, port = args.port)
    else:
        parser.print_help()
