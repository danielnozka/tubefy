class SongAlreadyDownloadedException(Exception):

    status_code = 409

    def __init__(self, song_id: str):

        super().__init__(f'Song with ID \'{song_id}\' already downloaded')
