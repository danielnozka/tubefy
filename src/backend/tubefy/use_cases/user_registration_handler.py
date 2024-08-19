import logging
from logging import Logger
from ..domain.user import User
from ..domain.user_credentials import UserCredentials
from ..exceptions.username_already_registered_exception import UsernameAlreadyRegisteredException
from ..persistence.i_users_repository import IUsersRepository


class UserRegistrationHandler:

    _log: Logger = logging.getLogger(__name__)
    _users_repository: IUsersRepository

    def __init__(self, users_repository: IUsersRepository) -> None:

        self._users_repository = users_repository

    async def register_user(self, user_credentials: UserCredentials) -> None:

        self._log.debug(f'Start [funcName](user_credentials={user_credentials})')

        if await self._users_repository.user_exists(user_credentials.username):

            raise UsernameAlreadyRegisteredException(user_credentials.username)

        else:

            await self._users_repository.add_user(user_credentials)

        self._log.debug(f'End [funcName](user_credentials={user_credentials})')
