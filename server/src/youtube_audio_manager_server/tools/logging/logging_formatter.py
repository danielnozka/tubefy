from logging import Formatter
from logging import LogRecord

from ..server import get_request_id


class LoggingFormatter(Formatter):

    _function_name_template = '[funcName]'

    def __init__(self, main_format: str, exception_format, date_format):

        self._main_format = main_format
        self._exception_format = exception_format
        super().__init__(fmt=main_format, datefmt=date_format)

    def format(self, record: LogRecord) -> str:

        self._select_format(record)
        record.correlation = get_request_id()
        record.msg = self._get_message_with_function_name(record)
        return super().format(record)

    def _select_format(self, record: LogRecord) -> None:

        if hasattr(record, 'exception'):

            self._style._fmt = self._exception_format

        else:

            self._style._fmt = self._main_format

    def _get_message_with_function_name(self, record: LogRecord) -> str:

        return record.msg.replace(self._function_name_template, record.funcName)
