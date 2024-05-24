import logging
from dependency_injector.wiring import inject, Provide
from logging import Logger
from ..adapters.audio_recording_adapter import AudioRecordingAdapter
from ..communications.youtube_audio_recording_getter import YoutubeAudioRecordingGetter
from ..domain.audio_recording import AudioRecording
from ..domain.user import User
from ..dtos.audio_download_options_input import AudioDownloadOptionsInput
from ..exceptions.audio_recording_already_downloaded_exception import AudioRecordingAlreadyDownloadedException
from ..persistence.audio_recordings_persistence import AudioRecordingsPersistence
from ..persistence.domain.audio_recording_persistence_domain import AudioRecordingPersistenceDomain


class AudioRecordingAdder:

    _log: Logger = logging.getLogger(__name__)
    _audio_recording_adapter: AudioRecordingAdapter
    _youtube_audio_recording_getter: YoutubeAudioRecordingGetter
    _audio_recordings_persistence: AudioRecordingsPersistence

    @inject
    def __init__(
        self,
        audio_recording_adapter: AudioRecordingAdapter = Provide['audio_recording_adapter'],
        youtube_audio_recording_getter: YoutubeAudioRecordingGetter = Provide['youtube_audio_recording_getter'],
        audio_recordings_persistence: AudioRecordingsPersistence = Provide['audio_recordings_persistence']
    ) -> None:

        self._audio_recording_adapter = audio_recording_adapter
        self._youtube_audio_recording_getter = youtube_audio_recording_getter
        self._audio_recordings_persistence = audio_recordings_persistence

    async def add(self, video_id: str, audio_download_options_input: AudioDownloadOptionsInput, user: User) -> None:

        self._log.debug(
            f'Start [funcName](video_id={video_id}, audio_download_options_input={audio_download_options_input}, '
            f'user={user})'
        )
        audio_recording: AudioRecording | None = next(
            (x for x in user.audio_recordings if x.video_id == video_id),
            None
        )

        if audio_recording is None:

            audio_recording: AudioRecording = self._youtube_audio_recording_getter.get(
                video_id=video_id,
                output_directory=(await self._audio_recordings_persistence.get_user_audio_recordings_directory(user)),
                output_filename=self._audio_recordings_persistence.get_audio_recording_filename(
                    audio_download_options_input
                ),
                audio_download_options_input=audio_download_options_input,
                user=user
            )
            audio_recording_persistence_domain: AudioRecordingPersistenceDomain = (
                self._audio_recording_adapter.adapt_to_persistence(
                    audio_recording=audio_recording,
                    user=user
                )
            )
            await self._audio_recordings_persistence.add_audio_recording(audio_recording_persistence_domain)
            self._log.debug(
                f'End [funcName](video_id={video_id}, audio_download_options_input={audio_download_options_input}, '
                f'user={user})'
            )

        else:

            raise AudioRecordingAlreadyDownloadedException(audio_recording)
