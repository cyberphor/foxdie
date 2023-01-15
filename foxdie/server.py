from foxdie.handlers import Handler, Listener

class Server:
    handlers: list[Handler]

    def start_handler(self, handler: Handler):
        handler.start()
        handler.stop()
