import logging

from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide
from logging import Logger
from uuid import UUID

from ..adapters.audio_adapter import AudioAdapter
from ..dtos.output_audio_recording import OutputAudioRecording
from ..exceptions.audio_recording_already_downloaded_exception import AudioRecordingAlreadyDownloadedException
from ..exceptions.audio_recording_not_found_exception import AudioRecordingNotFoundException
from .audio_downloader import AudioDownloader
from ..persistence.audio_persistence import AudioPersistence
from ..tools.typing import JsonType


class AudioService:

    _log: Logger = logging.getLogger(__name__)
    _audio_adapter: AudioAdapter
    _audio_downloader: AudioDownloader
    _audio_persistence: AudioPersistence

    @inject
    def __init__(self,
                 audio_adapter: AudioAdapter = Provide['audio_adapter'],
                 audio_downloader: AudioDownloader = Provide['audio_downloader'],
                 audio_persistence: AudioPersistence = Provide['audio_persistence']):

        self._audio_adapter = audio_adapter
        self._audio_downloader = audio_downloader
        self._audio_persistence = audio_persistence

    def download_audio_recording(self, user_id: UUID, video_id: str, input_data: JsonType) -> None:

        self._log.debug(f'Start [funcName](user_id=\'{user_id}\', video_id=\'{video_id}\')')
        audio_recording_exists = self._audio_persistence.get_audio_recording_by_video_id(user_id, video_id) is not None

        if audio_recording_exists:

            raise AudioRecordingAlreadyDownloadedException(user_id, video_id)

        else:

            input_audio_recording = self._audio_adapter.adapt_input(input_data)
            audio_recording = self._audio_downloader.download_audio_recording(user_id, video_id, input_audio_recording)
            self._audio_persistence.add_audio_recording(audio_recording)

        self._log.debug(f'End [funcName](user_id=\'{user_id}\', video_id=\'{video_id}\')')

    def get_all_audio_recordings(self, user_id: UUID) -> list[OutputAudioRecording]:

        self._log.debug(f'Start [funcName](user_id=\'{user_id}\')')
        audio_recordings = self._audio_persistence.get_all_audio_recordings(user_id)
        result = self._audio_adapter.adapt_output(audio_recordings)
        self._log.debug(f'End [funcName](user_id=\'{user_id}\')')

        return result

    def delete_audio_recording(self, user_id: UUID, video_id: str) -> None:

        self._log.debug(f'Start [funcName](user_id=\'{user_id}\', video_id=\'{video_id}\')')
        audio_recording = self._audio_persistence.get_audio_recording_by_video_id(user_id, video_id)

        if audio_recording is not None:

            self._audio_persistence.delete_audio_recording(audio_recording)

        else:

            raise AudioRecordingNotFoundException(user_id, video_id)

        self._log.debug(f'End [funcName](user_id=\'{user_id}\', video_id=\'{video_id}\')')
