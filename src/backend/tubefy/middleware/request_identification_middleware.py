from contextvars import ContextVar
from starlette.datastructures import MutableHeaders
from starlette.types import ASGIApp, Message, Scope, Receive, Send
from typing import Optional
from uuid import uuid4


class RequestIdentificationMiddleware:

    _request_id_context_var: ContextVar[Optional[str]] = ContextVar('requestId', default=None)
    _header_name: str = 'X-Request-ID'
    _app: ASGIApp

    def __init__(self, app: ASGIApp) -> None:

        self._app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:

        if scope['type'] not in ('http', 'websocket'):

            return await self._app(scope, receive, send)

        request_headers: MutableHeaders = MutableHeaders(scope=scope)
        request_id: str | None = request_headers.get(self._header_name)

        if request_id is None:

            request_id = str(uuid4())

        request_headers[self._header_name] = request_id
        self.set_request_id(request_id)

        async def handle_outgoing_request(message: Message) -> None:

            if message['type'] == 'http.response.start':

                response_headers: MutableHeaders = MutableHeaders(scope=message)
                response_headers.append(key=self._header_name, value=self.get_request_id())

            await send(message)

        await self._app(scope, receive, handle_outgoing_request)

    @classmethod
    def get_request_id(cls) -> str | None:

        return cls._request_id_context_var.get()

    @classmethod
    def set_request_id(cls, request_id: str) -> None:

        cls._request_id_context_var.set(request_id)
