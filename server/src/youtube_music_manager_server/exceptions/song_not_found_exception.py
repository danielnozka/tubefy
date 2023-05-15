class SongNotFoundException(Exception):

    status_code = 404

    def __init__(self, song_id: str):

        super().__init__(f'Song with ID \'{song_id}\' does not exist')
