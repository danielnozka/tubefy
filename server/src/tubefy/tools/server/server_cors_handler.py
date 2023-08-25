import cherrypy
import cherrypy_cors


class ServerCorsHandler:

    @staticmethod
    def setup() -> None:

        cherrypy_cors.install()

    @staticmethod
    def handle_options_request(**kwargs) -> None:

        cherrypy_cors.preflight(allowed_methods=[cherrypy.request.headers['Access-Control-Request-Method']])
