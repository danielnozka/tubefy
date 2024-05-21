import logging

from dependency_injector.wiring import inject, Provide
from logging import Logger

from ..adapters.user_adapter import UserAdapter
from ..dtos.user_input import UserInput
from ..exceptions.username_already_registered_exception import UsernameAlreadyRegisteredException
from ..persistence.users_persistence import UsersPersistence
from ..persistence.domain.user_persistence_domain import UserPersistenceDomain


class UserRegistrationHandler:

    _log: Logger = logging.getLogger(__name__)
    _user_adapter: UserAdapter
    _users_persistence: UsersPersistence

    @inject
    def __init__(
        self,
        user_adapter: UserAdapter = Provide['user_adapter'],
        users_persistence: UsersPersistence = Provide['users_persistence']
    ) -> None:

        self._user_adapter = user_adapter
        self._users_persistence = users_persistence

    async def register_user(self, user_input: UserInput) -> None:

        self._log.debug(f'Start [funcName](user_input={user_input})')

        user_persistence_domain: UserPersistenceDomain | None = (
            await self._users_persistence.get_user(user_input.username)
        )

        if user_persistence_domain is None:

            user_persistence_domain: UserPersistenceDomain = self._user_adapter.adapt_to_persistence(user_input)
            await self._users_persistence.add_user(user_persistence_domain)

        else:

            raise UsernameAlreadyRegisteredException(user_input.username)

        self._log.debug(f'End [funcName](user_input={user_input})')
