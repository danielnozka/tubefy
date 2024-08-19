from abc import ABC, abstractmethod
from ..domain.user import User
from ..domain.user_credentials import UserCredentials


class IUsersRepository(ABC):

    @abstractmethod
    async def user_exists(self, username: str) -> bool:

        raise NotImplementedError

    @abstractmethod
    async def get_user(self, user_credentials: UserCredentials) -> User | None:

        raise NotImplementedError

    @abstractmethod
    async def add_user(self, user_credentials: UserCredentials) -> None:

        raise NotImplementedError
