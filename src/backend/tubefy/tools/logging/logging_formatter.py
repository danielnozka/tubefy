from logging import Formatter, LogRecord


class LoggingFormatter(Formatter):

    _function_name_template: str = '[funcName]'
    _main_format: str
    _exception_format: str

    def __init__(self, main_format: str, exception_format, date_format):

        self._main_format = main_format
        self._exception_format = exception_format
        super().__init__(fmt=main_format, datefmt=date_format)

    def format(self, record: LogRecord) -> str:

        self._select_format(record)
        record.correlation = 'aaaa'
        record.msg = self._get_message_with_function_name(record)

        if self._record_has_exception(record):

            setattr(record, 'error', self._get_formatted_exception(record))

        return super().format(record)

    def _select_format(self, record: LogRecord) -> None:

        if self._record_has_exception(record):

            self._style._fmt = self._exception_format

        else:

            self._style._fmt = self._main_format

    @staticmethod
    def _record_has_exception(record: LogRecord) -> bool:

        return hasattr(record, 'exception')

    def _get_message_with_function_name(self, record: LogRecord) -> str:

        return record.msg.replace(self._function_name_template, record.funcName)

    @staticmethod
    def _get_formatted_exception(record: LogRecord) -> str:

        exception = getattr(record, 'exception')

        return f'{exception.__class__.__name__}: {exception}'
