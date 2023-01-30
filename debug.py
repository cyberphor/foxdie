from foxdie.servers import Server

def main():
    server = Server(ip = "127.0.0.1", port = 80)
    server.start()

if __name__ == "__main__":
    main()