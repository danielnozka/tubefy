import logging

from logging import Logger

from ..domain.authentication_credentials import AuthenticationCredentials
from ..domain.user import User
from ..dtos.output_authentication import OutputAuthentication
from ..tools.typing import JsonType


class AuthenticationAdapter:

    _log: Logger = logging.getLogger(__name__)

    def adapt_authentication_credentials(self, authentication_credentials_json: JsonType) -> AuthenticationCredentials:

        self._log.debug('Start [funcName]()')

        authentication_credentials = AuthenticationCredentials(username=authentication_credentials_json['username'],
                                                               password=authentication_credentials_json['password'])

        self._log.debug('End [funcName]()')

        return authentication_credentials

    def adapt_output_authentication(self, user: User) -> OutputAuthentication:

        self._log.debug('Start [funcName]()')
        result = OutputAuthentication(user_id=user.id, token=user.token)
        self._log.debug('End [funcName]()')

        return result
