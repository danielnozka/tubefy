import logging
from logging import Logger
from passlib.context import CryptContext


logging.getLogger('passlib').propagate = False


class PasswordHashHandler:

    _log: Logger = logging.getLogger(__name__)
    _context: CryptContext = CryptContext(schemes=['bcrypt'], deprecated='auto')

    def hash_password(self, password: str) -> str:

        self._log.debug('Start [funcName]()')
        result: str = self._context.hash(password)
        self._log.debug('End [funcName]()')

        return result

    def verify_password(self, password: str, hashed_password: str) -> bool:

        self._log.debug('Start [funcName]()')
        result: bool = self._context.verify(secret=password, hash=hashed_password)
        self._log.debug('End [funcName]()')

        return result
