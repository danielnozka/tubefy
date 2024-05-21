from .app_base_exception import AppBaseException


class AuthenticationRequiredException(AppBaseException):

    def __init__(self) -> None:

        super().__init__(status_code=401, message='Not authenticated', headers={'WWW-Authenticate': 'Bearer'})
