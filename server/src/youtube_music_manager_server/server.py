import cherrypy
import logging

from .exceptions.server_stopped_exception import ServerStoppedException
from .tools.server.server_routes_dispatcher import ServerRoutesDispatcher
from .tools.typing import ControllerInstanceType


cherrypy.log.error_log.propagate = False
cherrypy.log.access_log.propagate = False


class Server:

    def __init__(self, root_path: str, host: str, port: int):

        self._log = logging.getLogger(__name__)
        self._routes_dispatcher = ServerRoutesDispatcher()
        self._server_settings = {
            'global': {
                'server.socket_host': host,
                'server.socket_port': port,
                'log.screen': False,
                'log.access_file': '',
                'log.error_file': ''
            },
            '/': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': root_path,
                'request.dispatch': self._routes_dispatcher
            }
        }

    def start(self, testing: bool = False) -> None:

        self._log.debug('Starting server...')

        try:

            cherrypy.config.update(self._server_settings)
            cherrypy.tree.mount(self, '/', self._server_settings)
            cherrypy.engine.signals.subscribe()
            cherrypy.engine.start()
            self._log.debug('Server started successfully')

            if not testing:

                cherrypy.engine.block()

        except Exception as exception:

            self._log.error('Stopped server because of exception',
                            extra={'exception': f'{exception.__class__.__name__}: {exception}'})

            raise ServerStoppedException

    def register_controller(self, controller_instance: ControllerInstanceType) -> None:

        self._log.debug(f'Registering controller {controller_instance.__class__.__name__}...')
        self._routes_dispatcher.register_controller_instance(controller_instance)

    def stop(self) -> None:

        self._log.debug('Stopping server...')

        try:

            cherrypy.engine.exit()
            cherrypy.server.stop()
            self._log.debug('Server stopped successfully')

        except Exception as exception:

            self._log.error('Server stopping failed because of exception',
                            extra={'exception': f'{exception.__class__.__name__}: {exception}'})
