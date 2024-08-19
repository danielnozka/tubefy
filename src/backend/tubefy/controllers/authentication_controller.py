import logging
from datetime import datetime, timedelta
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends
from jose import jwt, JWTError
from logging import Logger
from ..adapters.user_credentials_adapter import UserCredentialsAdapter
from .app_base_controller import AppBaseController
from ..dtos.token_dto import TokenDto
from ..dtos.user_credentials_dto import UserCredentialsDto
from ..settings.json_web_token_settings import JsonWebTokenSettings
from ..use_cases.user_login_handler import UserLoginHandler
from ..use_cases.user_registration_handler import UserRegistrationHandler


class AuthenticationController(AppBaseController):

    _api_router: APIRouter = APIRouter(prefix='/api/auth', tags=['authentication'])
    _log: Logger = logging.getLogger(__name__)
    _user_credentials_adapter: UserCredentialsAdapter

    def __init__(self) -> None:

        self._api_router.add_api_route(path='/register', endpoint=self.register_user, methods=['POST'])
        self._api_router.add_api_route(path='/login', endpoint=self.log_in_user, methods=['POST'])
        self._user_credentials_adapter = UserCredentialsAdapter()

    @property
    def api_router(self) -> APIRouter:

        return self._api_router

    @inject
    async def register_user(
        self,
        user_credentials: UserCredentialsDto = Depends(),
        user_registration_handler: UserRegistrationHandler = Depends(Provide['user_registration_handler'])
    ) -> None:

        self._log.info(f'Start [funcName](user_credentials={user_credentials})')

        try:

            await user_registration_handler.register_user(
                self._user_credentials_adapter.adapt_user_credentials_from_dto(user_credentials)
            )
            self._log.info(f'End [funcName](user_credentials={user_credentials})')

        except Exception as exception:

            self._log.error(
                msg=f'End [funcName](user_credentials={user_credentials}) with exceptions',
                extra={'exception': exception}
            )

            raise exception

    @inject
    async def log_in_user(
        self,
        user_credentials: UserCredentialsDto = Depends(),
        user_login_handler: UserLoginHandler = Depends(Provide['user_login_handler'])
    ) -> TokenDto:

        self._log.info(f'Start [funcName](user_credentials={user_credentials})')

        try:

            await user_login_handler.log_in_user(
                self._user_credentials_adapter.adapt_user_credentials_from_dto(user_credentials)
            )
            settings: JsonWebTokenSettings = JsonWebTokenSettings()
            result: TokenDto = TokenDto(
                access_token=jwt.encode(
                    claims={
                        'sub': user_credentials.username,
                        'exp': (datetime.utcnow() + timedelta(minutes=settings.expiration_minutes))
                    },
                    key=settings.key,
                    algorithm=settings.algorithm
                ),
                token_type='bearer'
            )
            self._log.info(f'End [funcName](user_credentials={user_credentials})')

            return result

        except Exception as exception:

            self._log.error(
                msg=f'End [funcName](user_credentials={user_credentials}) with exceptions',
                extra={'exception': exception}
            )

            raise exception
