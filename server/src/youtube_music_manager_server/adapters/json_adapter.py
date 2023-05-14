import logging

from ..tools.typing import JsonType


class JsonAdapter:

    _log = logging.getLogger(__name__)

    def adapt(self, obj: object) -> JsonType:

        self._log.debug('Start [funcName]()')

        result = {}

        for attribute, value in obj.__dict__.items():

            result[self._snake_case_to_lower_camel_case(attribute)] = value

        self._log.debug('End [funcName]()')

        return result

    def _snake_case_to_lower_camel_case(self, snake_case_string: str) -> str:

        camel_case_string = self._snake_case_to_camel_case(snake_case_string)

        return snake_case_string[0].lower() + camel_case_string[1:]

    @staticmethod
    def _snake_case_to_camel_case(snake_case_string: str) -> str:

        return ''.join(x.capitalize() for x in snake_case_string.lower().split('_'))
