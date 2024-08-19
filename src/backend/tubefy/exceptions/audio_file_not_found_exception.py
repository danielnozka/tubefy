from pathlib import Path


class AudioFileNotFoundException(Exception):

    def __init__(self, audio_file_path: Path) -> None:

        super().__init__(f'Audio file \'{audio_file_path}\' does not exist')
