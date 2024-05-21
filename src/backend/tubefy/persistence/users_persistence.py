import logging

from dependency_injector.wiring import inject, Provide
from logging import Logger

from .app_persistence_context import AppPersistenceContext
from .domain.user_persistence_domain import UserPersistenceDomain


class UsersPersistence:

    _log: Logger = logging.getLogger(__name__)
    _context: AppPersistenceContext

    @inject
    def __init__(self, context: AppPersistenceContext = Provide['app_persistence_context']) -> None:

        self._context = context

    async def get_user(self, username: str) -> UserPersistenceDomain | None:

        self._log.debug(f'Start [funcName](username=\'{username}\')')
        result: UserPersistenceDomain | None = await self._context.get_user(username)
        self._log.debug(f'End [funcName](username=\'{username}\')')

        return result

    async def add_user(self, user: UserPersistenceDomain) -> None:

        self._log.debug(f'Start [funcName](user={user})')
        await self._context.add_user(user)
        self._log.debug(f'End [funcName](user={user})')
