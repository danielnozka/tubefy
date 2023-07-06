import cherrypy

from uuid import UUID

from ..typing import ControllerMethodType
from ..typing import JsonType


class ServerRequestHandler:

    @classmethod
    def get_request_id(cls) -> UUID:

        return cherrypy.request.unique_id.uuid4

    @classmethod
    def get_json_content(cls) -> JsonType:

        return cherrypy.request.json

    @classmethod
    def expect_json_content(cls, method: ControllerMethodType) -> ControllerMethodType:

        return cherrypy.tools.json_in()(method)
