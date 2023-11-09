import logging

from ..domain.user import User
from .tubefy_context import TubefyContext


class AuthenticationPersistence:

    _log = logging.getLogger(__name__)
    _context: TubefyContext

    def __init__(self):

        self._context = TubefyContext()

    def get_user_by_username(self, username: str) -> User | None:

        self._log.debug(f'Start [funcName](username=\'{username}\')')
        result = self._context.get_user_by_username(username)
        self._log.debug(f'End [funcName](username=\'{username}\')')

        return result

    def register_user(self, user: User) -> None:

        self._log.debug(f'Start [funcName]({user})')
        self._context.register_user(user)
        self._log.debug(f'End [funcName]({user})')
