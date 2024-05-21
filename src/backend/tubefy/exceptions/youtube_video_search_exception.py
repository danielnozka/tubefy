from .app_base_exception import AppBaseException


class YoutubeVideoSearchException(AppBaseException):

    def __init__(self, exception: Exception) -> None:

        super().__init__(status_code=500, message=f'{exception.__class__.__name__} - {exception}')
