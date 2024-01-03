import os


class ServerSettings:

    host: str
    port: int

    def __init__(self, host: str, port: int):

        self.host = os.environ.get('HOST', host)
        self.port = os.environ.get('PORT', port)
