import logging
import os

from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide

from ..configuration.app_settings import AppSettings
from ..domain.audio_recording import AudioRecording
from ..exceptions.audio_file_not_found_exception import AudioFileNotFoundException
from .audio_context import AudioContext


class AudioPersistence:

    _log = logging.getLogger(__name__)

    @inject
    def __init__(self, app_settings: AppSettings = Provide['app_settings']):

        self._context = AudioContext()
        self._audio_files_directory = os.path.abspath(app_settings.persistence_settings.audio_files_directory)

        if not self._audio_files_directory_exists():

            self._create_audio_files_directory()

    def get_audio_files_directory(self) -> str:

        return self._audio_files_directory

    def add_audio_recording(self, audio_recording: AudioRecording) -> None:

        self._log.debug(f'Start [funcName]({audio_recording})')
        self._context.add_audio_recording(audio_recording)
        self._log.debug(f'End [funcName]({audio_recording})')

    def get_all_audio_recordings(self) -> list[AudioRecording]:

        self._log.debug(f'Start [funcName]()')
        result = self._context.get_all_audio_recordings()
        self._log.debug(f'End [funcName]()')

        return result

    def get_audio_recording_by_id(self, audio_recording_id: str) -> AudioRecording | None:

        self._log.debug(f'Start [funcName](audio_recording_id=\'{audio_recording_id}\')')
        result = self._context.get_audio_recording_by_id(audio_recording_id)
        self._log.debug(f'End [funcName](audio_recording_id=\'{audio_recording_id}\')')

        return result

    def delete_audio_recording(self, audio_recording: AudioRecording) -> None:

        self._log.debug(f'Start [funcName]({audio_recording})')
        self._context.delete_audio_recording(audio_recording)
        self._delete_audio_recording_file(audio_recording)
        self._log.debug(f'End [funcName]({audio_recording})')

    def _audio_files_directory_exists(self) -> bool:

        return os.path.isdir(self._audio_files_directory)

    def _create_audio_files_directory(self) -> None:

        os.makedirs(self._audio_files_directory, exist_ok=True)

    @staticmethod
    def _delete_audio_recording_file(audio_recording: AudioRecording) -> None:

        if os.path.isfile(audio_recording.file):

            os.remove(audio_recording.file)

        else:

            raise AudioFileNotFoundException(audio_recording.file)
