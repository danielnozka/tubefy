from fastapi import Request
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer

from ..exceptions.authentication_required_exception import AuthenticationRequiredException


class RequestAuthenticationMiddleware:

    _authentication_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl='/api/auth/login')

    @classmethod
    async def authenticate_request(cls, request: Request) -> str:

        try:

            return await cls._authentication_scheme(request)

        except HTTPException:

            raise AuthenticationRequiredException
