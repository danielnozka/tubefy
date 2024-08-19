from ..domain.user_audio import UserAudio


class UserAudioAlreadyDownloadedException(Exception):

    def __init__(self, user_audio: UserAudio) -> None:

        super().__init__(
            f'Audio from video \'{user_audio.video_id}\' already downloaded for user \'{user_audio.user_id}\''
        )
