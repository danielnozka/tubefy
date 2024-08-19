class AudioDownloadException(Exception):

    def __init__(self) -> None:

        super().__init__('Audio download exceeded the maximum numbers of attempts')
