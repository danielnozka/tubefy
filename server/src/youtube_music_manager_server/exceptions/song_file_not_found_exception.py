class SongFileNotFoundException(Exception):

    status_code = 404

    def __init__(self, song_file: str):

        super().__init__(f'Song file \'{song_file}\' does not exist')
