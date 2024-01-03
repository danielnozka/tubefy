from .app_base_exception import AppBaseException


class UserUnauthorizedException(AppBaseException):

    def __init__(self, detail: str):

        super().__init__(status_code=401, detail=detail, headers={'WWW-Authenticate': 'Bearer'})
