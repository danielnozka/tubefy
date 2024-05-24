import logging
import logging.config
from logging import StreamHandler
from typing import Any
from .logging_request_identification_filter import LoggingRequestIdentificationFilter
from .logging_terminal_formatter import LoggingTerminalFormatter


class LoggingBuilder:

    _configuration: dict[str, Any] = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'request_identification_filter': {
                '()': LoggingRequestIdentificationFilter
            }
        },
        'formatters': {
            'terminal_formatter': {
                '()': LoggingTerminalFormatter,
            }
        },
        'handlers': {
            'terminal_handler': {
                'class': '.'.join([StreamHandler.__module__, StreamHandler.__name__]),
                'level': 'DEBUG',
                'formatter': 'terminal_formatter',
                'filters': ['request_identification_filter']
            }
        },
        'loggers': {
            'root': {
                'level': 'DEBUG',
                'handlers': [
                    'terminal_handler'
                ]
            }
        }
    }

    @classmethod
    def build(cls) -> None:

        logging.config.dictConfig(cls._configuration)

    @classmethod
    def get_configuration(cls) -> dict[str, Any]:

        return cls._configuration
