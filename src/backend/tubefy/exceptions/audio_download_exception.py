from .app_base_exception import AppBaseException


class AudioDownloadException(AppBaseException):

    def __init__(self):

        super().__init__(status_code=500, detail='Audio recording download exceeded the maximum numbers of attempts')
