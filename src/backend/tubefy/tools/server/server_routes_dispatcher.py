import cherrypy

from typing import Callable

from ...exceptions.controller_not_exposed_exception import ControllerNotExposedException
from .server_cors_handler import ServerCorsHandler
from ..typing import ControllerClassType
from ..typing import ControllerInstanceType
from ..typing import ControllerMethodType


class ServerRoutesDispatcher(cherrypy.dispatch.RoutesDispatcher):

    _exposed_controllers: dict = {}
    _server_cors_handler: ServerCorsHandler

    def __init__(self):

        super().__init__()
        self._server_cors_handler = ServerCorsHandler()
        self._server_cors_handler.setup()

    @classmethod
    def expose_controller_class(cls, controller_route: str) -> Callable[[ControllerClassType], ControllerClassType]:

        def _wrapped_controller_class(controller_class: ControllerClassType) -> ControllerClassType:

            cls._save_exposed_controller_class(controller_class, controller_route)

            return controller_class

        return _wrapped_controller_class

    @classmethod
    def expose_controller_http_get_method(cls, method_route: str) -> ControllerMethodType:

        return cls._expose_controller_http_method(method_route, 'GET')

    @classmethod
    def expose_controller_http_post_method(cls, method_route: str) -> ControllerMethodType:

        return cls._expose_controller_http_method(method_route, 'POST')

    @classmethod
    def expose_controller_http_put_method(cls, method_route: str) -> ControllerMethodType:

        return cls._expose_controller_http_method(method_route, 'PUT')

    @classmethod
    def expose_controller_http_delete_method(cls, method_route: str) -> ControllerMethodType:

        return cls._expose_controller_http_method(method_route, 'DELETE')

    def register_controller_instance(self, controller_instance: ControllerInstanceType) -> None:

        controller_name = controller_instance.__class__.__name__

        if controller_name in self._exposed_controllers:

            exposed_controller_info = self._exposed_controllers[controller_name]

            for method_name, method_info in exposed_controller_info['controller_methods'].items():

                self.connect(name=f'{controller_name}.{method_name}',
                             route=f"{exposed_controller_info['controller_route']}{method_info['method_route']}",
                             action=method_name,
                             controller=controller_instance,
                             conditions=method_info['method_type'])

                self.connect(name=f'{controller_name}.{method_name}.OPTIONS',
                             route=f"{exposed_controller_info['controller_route']}{method_info['method_route']}",
                             action='handle_options_request',
                             controller=self._server_cors_handler,
                             conditions=dict(method=['OPTIONS']))

        else:

            raise ControllerNotExposedException(controller_name)

    @classmethod
    def _save_exposed_controller_class(cls, controller_class: ControllerClassType, controller_route: str) -> None:

        controller_name = controller_class.__name__

        if cls._exposed_controller_class_already_saved(controller_name):

            cls._save_exposed_controller_class_route(controller_name, controller_route)

        else:

            cls._save_new_exposed_controller_class(controller_name, controller_route)

    @classmethod
    def _exposed_controller_class_already_saved(cls, controller_name: str) -> bool:

        return controller_name in cls._exposed_controllers

    @classmethod
    def _save_exposed_controller_class_route(cls, controller_name: str, controller_route: str) -> None:

        cls._exposed_controllers[controller_name]['controller_route'] = controller_route

    @classmethod
    def _save_new_exposed_controller_class(cls, controller_name: str, controller_route: str | None) -> None:

        cls._exposed_controllers[controller_name] = {'controller_route': controller_route, 'controller_methods': {}}

    @classmethod
    def _expose_controller_http_method(cls, method_route: str, method_type: str) -> ControllerMethodType:

        def _wrapped_controller_http_method(method: ControllerMethodType) -> ControllerMethodType:

            cls._save_exposed_controller_http_method(method, method_route, dict(method=[method_type]))

            return cherrypy.expose(cherrypy.tools.params()(method))

        return _wrapped_controller_http_method

    @classmethod
    def _save_exposed_controller_http_method(cls, method: ControllerMethodType, method_route: str,
                                             method_type: dict) -> None:

        controller_name, method_name = method.__qualname__.split('.')

        if not cls._exposed_controller_class_already_saved(controller_name):

            cls._save_new_exposed_controller_class(controller_name, controller_route=None)

        cls._save_new_exposed_controller_http_method(controller_name, method_name, method_route, method_type)

    @classmethod
    def _save_new_exposed_controller_http_method(cls, controller_name: str, method_name: str, method_route: str,
                                                 method_type: dict) -> None:

        cls._exposed_controllers[controller_name]['controller_methods'][method_name] = {'method_route': method_route,
                                                                                        'method_type': method_type}
