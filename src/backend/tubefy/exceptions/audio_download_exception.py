from .app_base_exception import AppBaseException


class AudioDownloadException(AppBaseException):

    def __init__(self) -> None:

        super().__init__(status_code=500, message='Audio recording download exceeded the maximum numbers of attempts')
