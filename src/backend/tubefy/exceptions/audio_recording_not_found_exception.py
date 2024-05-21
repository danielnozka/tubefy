from uuid import UUID

from .app_base_exception import AppBaseException


class AudioRecordingNotFoundException(AppBaseException):

    def __init__(self, audio_recording_id: UUID) -> None:

        super().__init__(status_code=404, message=f'Audio recording \'{audio_recording_id}\' does not exist')
