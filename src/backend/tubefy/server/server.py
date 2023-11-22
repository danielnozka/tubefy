import uvicorn

from fastapi import FastAPI

from . import ControllersRouter
from .domain import BaseController


class Server(FastAPI):

    _controllers_router: ControllersRouter = ControllersRouter()
    _host: str
    _port: int

    def __init__(self, host: str, port: int):

        self._host = host
        self._port = port
        super().__init__()

    def start(self) -> None:

        uvicorn.run(self, host=self._host, port=self._port)

    def register_controllers(self, app_controllers: list[type[BaseController]]) -> None:

        for AppController in app_controllers:

            app_controller = AppController()
            router = self._controllers_router.get_controller_router(app_controller)
            self.include_router(router)
