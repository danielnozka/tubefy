import cherrypy

from ..typing import ControllerMethodType


class ServerResponseHandler:

    @classmethod
    def return_json(cls, method: ControllerMethodType) -> ControllerMethodType:

        return cherrypy.tools.json_out()(method)

    @classmethod
    def return_exception(cls, exception: Exception = None) -> None:

        raise cherrypy.HTTPError(cls._get_exception_status_code(exception), cls._format_exception_message(exception))

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
