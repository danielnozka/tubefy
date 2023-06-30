class AudioFileNotFoundException(Exception):

    status_code: int = 404

    def __init__(self, audio_file: str):

        super().__init__(f'Audio file \'{audio_file}\' does not exist')
