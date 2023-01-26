from foxdie.servers import Server, Listener, Handler

def main():
    listener = Listener(ip = "127.0.0.1", port = 80)
    handler = Handler()
    server = Server(
        workers = {listener: handler}
    )
    server.bar()

if __name__ == "__main__":
    main()