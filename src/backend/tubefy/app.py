import logging
import uvicorn

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from logging import Logger
from pathlib import Path
from types import ModuleType
from uuid import uuid4

from . import adapters, communications, controllers, persistence, services, use_cases
from .controllers import APP_CONTROLLERS
from .exceptions import AppBaseException


logging.getLogger('asyncio').propagate = False
logging.getLogger('multipart').propagate = False

APP_COMPONENTS: list[ModuleType] = [adapters, communications, controllers, persistence, services, use_cases]
APP_ROOT_PATH: Path = Path(__file__).parent
APP_SETTINGS_FILE_PATH: Path = APP_ROOT_PATH.joinpath('app_settings.json')


class App(FastAPI):

    _log: Logger = logging.getLogger(__name__)
    _host: str
    _port: int

    def __init__(self, host: str, port: int):

        super().__init__(docs_url='/api/docs', openapi_url='/api/openapi.json')
        self.add_exception_handler(AppBaseException, self._handle_app_exception)
        self.add_exception_handler(Exception, self._handle_unexpected_exception)
        self._add_controllers()
        self._add_middleware()
        self._host = host
        self._port = port

    def start(self) -> None:

        self._log.info('Starting application...')

        try:

            uvicorn.run(self, host=self._host, port=self._port)

        except Exception as exception:

            self._log.error('Stopped application because of exception', extra={'exception': exception})

    def _add_controllers(self) -> None:

        for AppController in APP_CONTROLLERS:

            app_controller = AppController()
            self.include_router(app_controller.api_router)

    def _add_middleware(self) -> None:

        self.add_middleware(CorrelationIdMiddleware, generator=lambda: str(uuid4()))

    @staticmethod
    async def _handle_app_exception(request: Request, exc: AppBaseException) -> JSONResponse:

        return JSONResponse(status_code=exc.status_code, content=exc.detail, headers=exc.headers)

    @staticmethod
    async def _handle_unexpected_exception(request: Request, exc: Exception) -> JSONResponse:

        return JSONResponse(status_code=500, content=f'{exc.__class__.__name__}: {exc}')
