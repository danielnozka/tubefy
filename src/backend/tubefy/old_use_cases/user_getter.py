import logging
from dependency_injector.wiring import inject, Provide
from logging import Logger
from ..domain.user import User
from ..exceptions.unauthorized_user_exception import UnauthorizedUserException
from ..persistence.i_users_repository import IUsersRepository


class UserGetter:

    _log: Logger = logging.getLogger(__name__)
    _users_repository: IUsersRepository

    @inject
    def __init__(self, users_repository: IUsersRepository = Provide['users_repository']) -> None:

        self._users_repository = users_repository

    async def get_user(self, username: str) -> User:

        self._log.debug(f'Start [funcName](username=\'{username}\')')
        user: User | None = await self._users_repository.get_user(username)

        if user is None:

            raise UnauthorizedUserException('User not found')

        self._log.debug(f'End [funcName](username=\'{username}\')')

        return user
