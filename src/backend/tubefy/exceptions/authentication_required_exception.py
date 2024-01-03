from .app_base_exception import AppBaseException


class AuthenticationRequiredException(AppBaseException):

    def __init__(self):

        super().__init__(status_code=401, detail='Not authenticated', headers={'WWW-Authenticate': 'Bearer'})
