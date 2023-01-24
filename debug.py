from threading import Event
from foxdie.servers import Server, Listener, Handler

def main():
    event = Event()
    server = Server(
        killswitch = event,
        listener = Listener(
            killswitch = event,
            ip = "127.0.0.1", 
            port = 80, 
            handler = Handler
        )
    )
    server.start()

if __name__ == "__main__":
    main()