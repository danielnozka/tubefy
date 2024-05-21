from logging import Formatter, LogRecord


class LoggingTerminalFormatter(Formatter):

    _function_name_template: str = '[funcName]'
    _date_format: str = '%d-%m-%Y %H:%M:%S'
    _main_format_without_request_identification: str = (
        '%(asctime)s.%(msecs)03d - [%(levelname)s] - [%(name)s] - %(message)s'
    )
    _main_format_with_request_identification: str = (
        '%(asctime)s.%(msecs)03d - [%(levelname)s] - [%(request)s] - [%(name)s] - %(message)s'
    )
    _exception_format_without_request_identification: str = (
        '%(asctime)s.%(msecs)03d - [%(levelname)s] - [%(name)s] - %(message)s - %(error)s'
    )
    _exception_format_with_request_identification: str = (
        '%(asctime)s.%(msecs)03d - [%(levelname)s] - [%(request)s] - [%(name)s] - %(message)s - %(error)s'
    )

    def __init__(self) -> None:

        super().__init__(fmt=self._main_format_without_request_identification, datefmt=self._date_format)

    def format(self, record: LogRecord) -> str:

        self._select_format(record)
        record.msg = self._format_message(record)

        if self._record_has_exception(record):
            setattr(record, 'error', self._format_exception(record))

        return super().format(record)

    def _select_format(self, record: LogRecord) -> None:

        if self._record_has_exception(record):

            if self._record_has_request_id(record):

                self._style._fmt = self._exception_format_with_request_identification

            else:

                self._style._fmt = self._exception_format_without_request_identification

        else:

            if self._record_has_request_id(record):

                self._style._fmt = self._main_format_with_request_identification

            else:

                self._style._fmt = self._main_format_without_request_identification

    @staticmethod
    def _record_has_exception(record: LogRecord) -> bool:

        return hasattr(record, 'exception')

    @staticmethod
    def _record_has_request_id(record: LogRecord) -> bool:

        return hasattr(record, 'request')

    def _format_message(self, record: LogRecord) -> str:

        return self._format_quotation_marks(self._format_function_name(record))

    def _format_function_name(self, record: LogRecord) -> str:

        return record.msg.replace(self._function_name_template, record.funcName)

    @staticmethod
    def _format_quotation_marks(message: str) -> str:

        return message.replace('"', "'")

    @staticmethod
    def _format_exception(record: LogRecord) -> str:

        exception: Exception = getattr(record, 'exception')

        return f'{exception.__class__.__name__}: {exception}'
