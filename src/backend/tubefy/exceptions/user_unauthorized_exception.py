from .app_base_exception import AppBaseException


class UserUnauthorizedException(AppBaseException):

    def __init__(self, detail: str) -> None:

        super().__init__(status_code=401, message=detail, headers={'WWW-Authenticate': 'Bearer'})
