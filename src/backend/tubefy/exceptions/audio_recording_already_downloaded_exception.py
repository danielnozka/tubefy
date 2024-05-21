from ..domain.audio_recording import AudioRecording
from .app_base_exception import AppBaseException


class AudioRecordingAlreadyDownloadedException(AppBaseException):

    def __init__(self, audio_recording: AudioRecording) -> None:

        super().__init__(
            status_code=409,
            message=(
                f'Audio from video \'{audio_recording.video_id}\' already downloaded '
                f'for user \'{audio_recording.user_id}\''
            )
        )
