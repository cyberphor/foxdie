from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
from concurrent.futures import ThreadPoolExecutor

def handler(agent_socket: socket, agent_port: int):
    while True:
        agent_request = agent_socket.recv(1024)
        print(agent_request)
        if not agent_request:
            agent_socket.close()
            break
        agent_socket.sendall(agent_port)

def main():
    ip = "127.0.0.1"
    port = 80
    address = (str(ip), port)
    with socket(AF_INET, SOCK_STREAM) as listener:
        listener.bind(address)
        listener.listen(5)
        agent_socket, agent_port = listener.accept()
        agent_thread = Thread(
            name = agent_port, 
            target = handler, 
            args = (agent_socket, agent_port)
        )

if __name__ == "__main__":
	main()