import logging
from logging import Logger
from ..domain.user import User
from ..domain.user_credentials import UserCredentials
from ..exceptions.unauthorized_user_exception import UnauthorizedUserException
from ..persistence.i_users_repository import IUsersRepository


class UserLoginHandler:

    _log: Logger = logging.getLogger(__name__)
    _users_repository: IUsersRepository

    def __init__(self, users_repository: IUsersRepository) -> None:

        self._users_repository = users_repository

    async def log_in_user(self, user_credentials: UserCredentials) -> User:

        self._log.debug(f'Start [funcName](user_credentials={user_credentials})')
        user: User | None = await self._users_repository.get_user(user_credentials)

        if user is None:

            raise UnauthorizedUserException('Incorrect username or password')

        else:

            self._log.debug(f'End [funcName](user_credentials={user_credentials})')

            return user
