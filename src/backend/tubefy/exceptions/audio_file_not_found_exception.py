from pathlib import Path

from .app_base_exception import AppBaseException


class AudioFileNotFoundException(AppBaseException):

    def __init__(self, audio_file_path: Path) -> None:

        super().__init__(status_code=404, message=f'Audio file \'{audio_file_path}\' does not exist')
