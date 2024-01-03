import logging

from datetime import datetime, timedelta
from jose import jwt, JWTError
from logging import Logger

from ..exceptions import UserUnauthorizedException


class JsonWebTokenHandler:

    _log: Logger = logging.getLogger(__name__)
    _secret_key: str = 'cb02e341df3bec4f3fa0711d5c9a051700c5a09dc4fc05025780b4a595f89501'
    _algorithm: str = 'HS256'
    _access_token_expiration_minutes: int = 60

    def get_token(self, username: str) -> str:

        self._log.debug(f'Start [funcName](username=\'{username}\')')
        result = jwt.encode(
            claims=self._adapt_input_payload(username),
            key=self._secret_key,
            algorithm=self._algorithm
        )
        self._log.debug(f'End [funcName](username=\'{username}\')')

        return result

    def get_username(self, token: str) -> str:

        self._log.debug('Start [funcName]()')

        try:

            payload = jwt.decode(token=token, key=self._secret_key, algorithms=self._algorithm)
            result = self._adapt_output_payload(payload)

            if result is not None:

                self._log.debug('End [funcName]()')

                return result

        except JWTError:

            pass

        raise UserUnauthorizedException('Could not validate credentials')

    def _adapt_input_payload(self, username: str) -> dict[str, str | datetime]:

        return {
            'sub': username,
            'exp': self._get_expiration_datetime()
        }

    def _get_expiration_datetime(self) -> datetime:

        return datetime.utcnow() + timedelta(minutes=self._access_token_expiration_minutes)

    @staticmethod
    def _adapt_output_payload(payload: dict[str, str | datetime]) -> str | None:

        return payload.get('sub')
