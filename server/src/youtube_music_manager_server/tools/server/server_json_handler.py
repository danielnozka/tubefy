import cherrypy

from .server_json_adapter import ServerJsonAdapter
from .server_json_encoder import ServerJsonEncoder


class ServerJsonHandler:

    @classmethod
    def handle(cls) -> bytes:

        obj = cherrypy.serving.request.inner_handler()
        json_obj = ServerJsonAdapter.adapt(obj)

        return ServerJsonEncoder.encode(json_obj)
