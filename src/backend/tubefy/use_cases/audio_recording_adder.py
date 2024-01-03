import logging

from dependency_injector.wiring import inject, Provide
from logging import Logger

from ..adapters import AudioRecordingAdapter
from ..communications import YoutubeAudioDownloader
from ..domain import User
from ..dtos import AudioDownloadOptionsInput
from ..exceptions import AudioRecordingAlreadyDownloadedException
from ..persistence import AudioRecordingsPersistence


class AudioRecordingAdder:

    _log: Logger = logging.getLogger(__name__)
    _audio_recording_adapter: AudioRecordingAdapter
    _youtube_audio_downloader: YoutubeAudioDownloader
    _audio_recordings_persistence: AudioRecordingsPersistence

    @inject
    def __init__(
        self,
        audio_recording_adapter: AudioRecordingAdapter = Provide['audio_recording_adapter'],
        youtube_audio_downloader: YoutubeAudioDownloader = Provide['youtube_audio_downloader'],
        audio_recordings_persistence: AudioRecordingsPersistence = Provide['audio_recordings_persistence']
    ):

        self._audio_recording_adapter = audio_recording_adapter
        self._youtube_audio_downloader = youtube_audio_downloader
        self._audio_recordings_persistence = audio_recordings_persistence

    def add(self, video_id: str, audio_download_options_input: AudioDownloadOptionsInput, user: User) -> None:

        self._log.debug(
            f'Start [funcName](video_id={video_id}, audio_download_options_input={audio_download_options_input}, '
            f'user={user})'
        )
        audio_recording = next((x for x in user.audio_recordings if x.video_id == video_id), None)

        if audio_recording is None:

            audio_recording = self._youtube_audio_downloader.download_audio_recording(
                video_id=video_id,
                output_directory=self._audio_recordings_persistence.get_user_audio_recordings_directory(user),
                output_filename=self._audio_recordings_persistence.get_audio_recording_filename(
                    audio_download_options_input
                ),
                audio_download_options_input=audio_download_options_input,
                user=user
            )
            database_audio_recording = self._audio_recording_adapter.adapt_to_persistence(
                audio_recording=audio_recording,
                user=user
            )
            self._audio_recordings_persistence.add_audio_recording(database_audio_recording)
            self._log.debug(
                f'End [funcName](video_id={video_id}, audio_download_options_input={audio_download_options_input}, '
                f'user={user})'
            )

        else:

            raise AudioRecordingAlreadyDownloadedException(audio_recording)
