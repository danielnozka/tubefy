import logging
import jwt

from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide
from logging import Logger
from uuid import uuid4

from ..adapters.authentication_adapter import AuthenticationAdapter
from ..configuration.app_settings import AppSettings
from ..domain.authentication_credentials import AuthenticationCredentials
from ..domain.user import User
from ..dtos.output_authentication import OutputAuthentication
from ..exceptions.username_already_registered_exception import UsernameAlreadyRegisteredException
from ..exceptions.invalid_authentication_credentials_exception import InvalidAuthenticationCredentialsException
from ..persistence.authentication_persistence import AuthenticationPersistence
from ..tools.typing import JsonType


class AuthenticationService:

    _log: Logger = logging.getLogger(__name__)
    _json_web_token_secret_key: str
    _authentication_adapter: AuthenticationAdapter
    _authentication_persistence: AuthenticationPersistence

    @inject
    def __init__(self,
                 app_settings: AppSettings = Provide['app_settings'],
                 authentication_adapter: AuthenticationAdapter = Provide['authentication_adapter'],
                 authentication_persistence: AuthenticationPersistence = Provide['authentication_persistence']):

        self._json_web_token_secret_key = app_settings.authentication_settings.json_web_token_secret_key
        self._authentication_adapter = authentication_adapter
        self._authentication_persistence = authentication_persistence

    def login(self, authentication_credentials_json: JsonType) -> OutputAuthentication:

        self._log.debug('Start [funcName]()')

        authentication_credentials = \
            self._authentication_adapter.adapt_authentication_credentials(authentication_credentials_json)

        user = self._authentication_persistence.get_user_by_username(authentication_credentials.username)

        if user is None:

            raise InvalidAuthenticationCredentialsException

        else:

            if self._user_is_authorized(user, authentication_credentials):

                result = self._authentication_adapter.adapt_output_authentication(user)

            else:

                raise InvalidAuthenticationCredentialsException

        self._log.debug('End [funcName]()')

        return result

    def register(self, authentication_credentials_json: JsonType) -> None:

        self._log.debug('Start [funcName]()')

        authentication_credentials = \
            self._authentication_adapter.adapt_authentication_credentials(authentication_credentials_json)

        user = self._authentication_persistence.get_user_by_username(authentication_credentials.username)

        if user is not None:

            raise UsernameAlreadyRegisteredException(authentication_credentials.username)

        else:

            token = self._get_token(authentication_credentials)
            user = User(id_=uuid4(), username=authentication_credentials.username, token=token)
            self._authentication_persistence.register_user(user)

        self._log.debug('End [funcName]()')

    def _user_is_authorized(self, user: User, authentication_credentials: AuthenticationCredentials) -> bool:

        token = self._get_token(authentication_credentials)

        return token == user.token

    def _get_token(self, authentication_credentials: AuthenticationCredentials) -> str:

        payload = {
            'username': authentication_credentials.username,
            'password': authentication_credentials.password
        }

        token = jwt.encode(payload, key=self._json_web_token_secret_key)

        return token
