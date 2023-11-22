from fastapi import APIRouter

from typing import Any
from typing import Callable

from .domain import BaseController, ExposedController, ExposedMethod, HttpMethod


class ControllersRouter:

    _exposed_controllers: list[ExposedController] = []
    _http_method: HttpMethod = HttpMethod

    @classmethod
    def expose_controller_class(cls, controller_route: str) -> Callable[[type], type]:

        def _wrapped_controller_class(controller_class: type) -> type:

            cls._register_exposed_controller_class(controller_class, controller_route)

            return controller_class

        return _wrapped_controller_class

    @classmethod
    def expose_controller_http_delete_method(cls, method_route: str) -> Callable[..., Any]:

        return cls._expose_controller_http_method(method_route, cls._http_method.delete)

    @classmethod
    def expose_controller_http_get_method(cls, method_route: str) -> Callable[..., Any]:

        return cls._expose_controller_http_method(method_route, cls._http_method.get)

    @classmethod
    def expose_controller_http_post_method(cls, method_route: str) -> Callable[..., Any]:

        return cls._expose_controller_http_method(method_route, cls._http_method.post)

    @classmethod
    def expose_controller_http_put_method(cls, method_route: str) -> Callable[..., Any]:

        return cls._expose_controller_http_method(method_route, cls._http_method.put)

    def get_controller_router(self, controller_instance: BaseController) -> APIRouter:

        controller_name = controller_instance.__class__.__name__
        exposed_controller = self._get_exposed_controller_by_name(controller_name)
        router = APIRouter(prefix=exposed_controller.route)

        for exposed_method in exposed_controller.exposed_methods:

            router.add_api_route(
                path=exposed_method.route,
                endpoint=getattr(controller_instance, exposed_method.name),
                methods=[exposed_method.http_method.value]
            )

        return router

    @classmethod
    def _register_exposed_controller_class(cls, controller_class: type, controller_route: str) -> None:

        controller_name = controller_class.__name__

        if cls._exposed_controller_class_already_registered(controller_name):

            cls._update_exposed_controller_class_route(controller_name, controller_route)

        else:

            cls._register_new_exposed_controller_class(controller_name, controller_route)

    @classmethod
    def _exposed_controller_class_already_registered(cls, controller_name: str) -> bool:

        return cls._get_exposed_controller_by_name(controller_name) is not None

    @classmethod
    def _update_exposed_controller_class_route(cls, controller_name: str, controller_route: str) -> None:

        exposed_controller = cls._get_exposed_controller_by_name(controller_name)
        exposed_controller.route = controller_route

    @classmethod
    def _register_new_exposed_controller_class(cls, controller_name: str, controller_route: str | None) -> None:

        exposed_controller = ExposedController(controller_name, controller_route)
        cls._exposed_controllers.append(exposed_controller)

    @classmethod
    def _get_exposed_controller_by_name(cls, controller_name: str) -> ExposedController | None:

        return next((x for x in cls._exposed_controllers if x.name == controller_name), None)

    @classmethod
    def _expose_controller_http_method(cls, method_route: str, method_type: HttpMethod):

        def _wrapped_controller_http_method(method: Callable) -> Callable:

            cls._register_exposed_controller_http_method(method, method_route, method_type)

            return method

        return _wrapped_controller_http_method

    @classmethod
    def _register_exposed_controller_http_method(cls,
                                                 method: Callable,
                                                 method_route: str,
                                                 method_type: HttpMethod) -> None:

        controller_name, method_name = method.__qualname__.split('.')

        if not cls._exposed_controller_class_already_registered(controller_name):

            cls._register_new_exposed_controller_class(controller_name, controller_route=None)

        cls._register_new_exposed_controller_http_method(controller_name, method_name, method_route, method_type)

    @classmethod
    def _register_new_exposed_controller_http_method(cls,
                                                     controller_name: str,
                                                     method_name: str,
                                                     method_route: str,
                                                     method_type: HttpMethod) -> None:

        exposed_method = ExposedMethod(method_name, method_route, method_type)
        exposed_controller = cls._get_exposed_controller_by_name(controller_name)
        exposed_controller.exposed_methods.append(exposed_method)
