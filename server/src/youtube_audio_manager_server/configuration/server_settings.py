class ServerSettings:

    def __init__(self, host: str, port: int):

        self.host = host if host != 'localhost' else '0.0.0.0'
        self.port = port
