import cherrypy

from ..typing import MethodType


class ServerResponseHandler:

    @classmethod
    def return_json(cls, method: MethodType) -> MethodType:

        return cherrypy.tools.json_out()(method)

    @classmethod
    def return_exception(cls, status=500, exception: Exception = None) -> None:

        raise cherrypy.HTTPError(status, cls._format_exception_message(exception))

    @staticmethod
    def _format_exception_message(exception: Exception | None) -> str | None:

        message = None

        if exception is not None:

            message = str(exception)

        return message
