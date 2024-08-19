import logging
from logging import Logger
from ..dtos.token_dto import TokenOutput


class TokenAdapter:

    _log: Logger = logging.getLogger(__name__)

    def adapt(self, token: str) -> TokenOutput:

        self._log.debug('Start [funcName]()')
        result: TokenOutput = TokenOutput(access_token=token, token_type='bearer')
        self._log.debug('End [funcName]()')

        return result
