class AudioDownloadException(Exception):

    def __init__(self):

        super().__init__('Audio recording download exceeded the maximum numbers of attempts')
