from argparse import ArgumentParser
from foxdie.agents import Agent
from foxdie.servers import Server
from ipaddress import IPv4Address

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-m", "--mode", type = str, choices = ["server", "agent"])
    parser.add_argument("-i", "--ip-address", type = IPv4Address, required = True)
    parser.add_argument("-p", "--port", type = int, required = True)
    parser.add_argument("-c", "--command", type = str, choices = ["get", "post", "put", "head", "delete", "patch", "options"])
    args = parser.parse_args()
    if args.mode == "server":
        server = Server(
            ip = args.ip_address,
            port = args.port
        )
        server.start()
    elif args.mode == "agent":
        agent = Agent(
            server_ip = args.ip_address,
            server_port = args.port,
            request = args.command
        )
        agent.start()
    else:
        parser.print_help()
