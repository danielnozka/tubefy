import cherrypy

from .server_json_handler import ServerJsonHandler
from ..typing import ControllerMethodType


class ServerResponseHandler:

    @classmethod
    def return_json(cls, method: ControllerMethodType) -> ControllerMethodType:

        return cherrypy.tools.set_json_response()(method)

    @classmethod
    def return_exception(cls, exception: Exception = None) -> None:

        raise cherrypy.HTTPError(cls._get_exception_status_code(exception), cls._format_exception_message(exception))

    @staticmethod
    def set_json_response() -> None:

        request = cherrypy.serving.request
        request.inner_handler = request.handler
        request.handler = ServerJsonHandler.handle
        cherrypy.serving.response.headers['Content-Type'] = 'application/json'

    @classmethod
    def _get_exception_status_code(cls, exception: Exception) -> int:

        if cls._is_custom_exception(exception):

            return getattr(exception, 'status_code')

        else:

            return 500

    @staticmethod
    def _is_custom_exception(exception: Exception) -> bool:

        return hasattr(exception, 'status_code')

    @staticmethod
    def _format_exception_message(exception: Exception | None) -> str | None:

        message = None

        if exception is not None:

            message = str(exception)

        return message


cherrypy.tools.set_json_response = cherrypy.Tool('before_handler', ServerResponseHandler.set_json_response)
