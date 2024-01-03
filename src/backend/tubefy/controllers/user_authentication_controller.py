import logging

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from logging import Logger

from .app_base_controller import AppBaseController
from ..dtos import TokenOutput, UserInput
from ..exceptions import AuthenticationRequiredException
from ..use_cases import UserLoginHandler, UserRegistrationHandler


class UserAuthenticationController(AppBaseController):

    api_router: APIRouter = APIRouter(prefix='/api/auth', tags=['user_authentication'])
    _authentication_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl='/api/auth/login')
    _log: Logger = logging.getLogger(__name__)
    _user_login_handler: UserLoginHandler
    _user_registration_handler: UserRegistrationHandler

    @inject
    def __init__(
        self,
        user_login_handler: UserLoginHandler = Provide['user_login_handler'],
        user_registration_handler: UserRegistrationHandler = Provide['user_registration_handler']
    ):

        self.api_router.add_api_route(
            path='/register',
            endpoint=self.register_user,
            methods=['POST']
        )
        self.api_router.add_api_route(
            path='/login',
            endpoint=self.log_in_user,
            methods=['POST']
        )
        self._user_login_handler = user_login_handler
        self._user_registration_handler = user_registration_handler

    @classmethod
    async def authenticate_request(cls, request: Request) -> str:

        try:

            return await cls._authentication_scheme(request)

        except Exception:

            raise AuthenticationRequiredException

    async def register_user(self, user_input: UserInput = Depends()) -> None:

        self._log.info(f'Start [funcName](user_input={user_input})')

        try:

            self._user_registration_handler.register_user(user_input)
            self._log.info(f'End [funcName](user_input={user_input})')

        except Exception as exception:

            self._log.error(f'End [funcName](user_input={user_input}) with exceptions', extra={'exception': exception})

            raise exception

    async def log_in_user(self, user_input: UserInput = Depends()) -> TokenOutput:

        self._log.info(f'Start [funcName](user_input={user_input})')

        try:

            result = self._user_login_handler.log_in_user(user_input)
            self._log.info(f'End [funcName](user_input={user_input})')

            return result

        except Exception as exception:

            self._log.error(f'End [funcName](user_input={user_input}) with exceptions', extra={'exception': exception})

            raise exception
