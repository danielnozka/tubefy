from logging import Filter, LogRecord

from ..middleware.request_identification_middleware import RequestIdentificationMiddleware


class LoggingRequestIdentificationFilter(Filter):

    def filter(self, record: LogRecord) -> bool:

        request_id: str | None = RequestIdentificationMiddleware.get_request_id()

        if request_id is not None:

            setattr(record, 'request', request_id)

        return True
