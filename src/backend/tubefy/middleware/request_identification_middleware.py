from contextvars import ContextVar
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Awaitable, Callable, Optional, TypeAlias
from uuid import uuid4


RequestResponseEndpoint: TypeAlias = Callable[[Request], Awaitable[Response]]


class RequestIdentificationMiddleware(BaseHTTPMiddleware):

    _request_id_context_var: ContextVar[Optional[str]] = ContextVar('requestId', default=None)
    _header_name: str = 'X-Request-ID'

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:

        self.set_request_id(request.headers.get(self._header_name, str(uuid4())))
        response: Response = await call_next(request)
        response.headers[self._header_name] = self.get_request_id()

        return response

    @classmethod
    def get_request_id(cls) -> str | None:

        return cls._request_id_context_var.get()

    @classmethod
    def set_request_id(cls, request_id: str) -> None:

        cls._request_id_context_var.set(request_id)
