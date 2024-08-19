import logging
from logging import Logger
from ..domain.user_credentials import UserCredentials
from ..dtos.user_credentials_dto import UserCredentialsDto


class UserCredentialsAdapter:

    _log: Logger = logging.getLogger(__name__)

    def adapt_user_credentials_from_dto(self, user_credentials: UserCredentialsDto) -> UserCredentials:

        self._log.debug(f'Start [funcName](user_credentials={user_credentials})')
        result: UserCredentials = UserCredentials(
            username=user_credentials.username,
            password=user_credentials.password
        )
        self._log.debug(f'End [funcName](user_credentials={user_credentials})')

        return result
