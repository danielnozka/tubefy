from ..domain import AudioRecording
from .app_base_exception import AppBaseException


class AudioRecordingAlreadyDownloadedException(AppBaseException):

    def __init__(self, audio_recording: AudioRecording):

        super().__init__(
            status_code=409,
            detail=(
                f'Audio from video \'{audio_recording.video_id}\' already downloaded '
                f'for user \'{audio_recording.user_id}\''
            )
        )
