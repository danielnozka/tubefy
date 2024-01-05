import logging

from datetime import datetime, timedelta
from dependency_injector.wiring import inject, Provide
from jose import jwt, JWTError
from logging import Logger

from ..configuration import AppSettings
from ..exceptions import UserUnauthorizedException


class JsonWebTokenHandler:

    _log: Logger = logging.getLogger(__name__)
    _algorithm: str
    _expiration_minutes: float
    _key: str

    @inject
    def __init__(self, app_settings: AppSettings = Provide['app_settings']):

        self._algorithm = app_settings.security_settings.json_web_token_algorithm
        self._expiration_minutes = app_settings.security_settings.json_web_token_expiration_minutes
        self._key = app_settings.security_settings.json_web_token_key

    def get_token(self, username: str) -> str:

        self._log.debug(f'Start [funcName](username=\'{username}\')')
        result = jwt.encode(
            claims=self._adapt_input_payload(username),
            key=self._key,
            algorithm=self._algorithm
        )
        self._log.debug(f'End [funcName](username=\'{username}\')')

        return result

    def get_username(self, token: str) -> str:

        self._log.debug('Start [funcName]()')

        try:

            payload = jwt.decode(token=token, key=self._key, algorithms=self._algorithm)
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

        return datetime.utcnow() + timedelta(minutes=self._expiration_minutes)

    @staticmethod
    def _adapt_output_payload(payload: dict[str, str | datetime]) -> str | None:

        return payload.get('sub')
