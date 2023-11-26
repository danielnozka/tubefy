from .controllers_router import ControllersRouter
from .domain import BaseController, BaseInputDto, BaseOutputDto, FileDto
from .server import Server


route = ControllersRouter.expose_controller_class
http_get = ControllersRouter.expose_controller_http_get_method
http_delete = ControllersRouter.expose_controller_http_delete_method
http_post = ControllersRouter.expose_controller_http_post_method
http_put = ControllersRouter.expose_controller_http_put_method
