import logging

from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide
from logging import Logger

from ..dtos.output_authentication import OutputAuthentication
from ..tools.server import expect_json
from ..tools.server import get_json_content
from ..tools.server import http_post
from ..tools.server import return_exception
from ..tools.server import return_json
from ..tools.server import route
from ..use_cases.authentication_service import AuthenticationService


@route('')
class AuthenticationController:

    _log: Logger = logging.getLogger(__name__)
    _authentication_service: AuthenticationService

    @inject
    def __init__(self, authentication_service: AuthenticationService = Provide['authentication_service']):

        self._authentication_service = authentication_service

    @http_post('/login')
    @expect_json
    @return_json
    def login(self) -> OutputAuthentication:

        self._log.info('Start [funcName]()')

        try:

            result = self._authentication_service.login(get_json_content())
            self._log.info('End [funcName]()')

            return result

        except Exception as exception:

            self._log.error('End [funcName]() with exceptions', extra={'exception': exception})

            return_exception(exception)

    @http_post('/register')
    @expect_json
    def register(self) -> None:

        self._log.info('Start [funcName]()')

        try:

            self._authentication_service.register(get_json_content())
            self._log.info('End [funcName]()')

        except Exception as exception:

            self._log.error('End [funcName]() with exceptions', extra={'exception': exception})

            return_exception(exception)
