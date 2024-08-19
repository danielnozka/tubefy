class YoutubeVideosRepositoryException(Exception):

    def __init__(self, exception: Exception) -> None:

        super().__init__(f'{exception.__class__.__name__} - {exception}')
