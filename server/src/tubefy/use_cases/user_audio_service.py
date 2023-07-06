import logging

from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide
from logging import Logger
from uuid import UUID
from uuid import uuid4

from ..adapters.user_audio_adapter import UserAudioAdapter
from ..communications.youtube_audio_downloader import YoutubeAudioDownloader
from ..domain.audio_recording import AudioRecording
from ..dtos.output_audio_recording import OutputAudioRecording
from ..exceptions.audio_recording_already_downloaded_exception import AudioRecordingAlreadyDownloadedException
from ..exceptions.audio_recording_not_found_exception import AudioRecordingNotFoundException
from ..persistence.user_audio_persistence import UserAudioPersistence
from ..tools.typing import JsonType


class UserAudioService:

    _log: Logger = logging.getLogger(__name__)
    _user_audio_adapter: UserAudioAdapter
    _youtube_audio_downloader: YoutubeAudioDownloader
    _user_audio_persistence: UserAudioPersistence

    @inject
    def __init__(self,
                 user_audio_adapter: UserAudioAdapter = Provide['user_audio_adapter'],
                 youtube_audio_downloader: YoutubeAudioDownloader = Provide['youtube_audio_downloader'],
                 user_audio_persistence: UserAudioPersistence = Provide['user_audio_persistence']):

        self._user_audio_adapter = user_audio_adapter
        self._youtube_audio_downloader = youtube_audio_downloader
        self._user_audio_persistence = user_audio_persistence

    def save_user_audio_recording(self, user_id: UUID, video_id: str, audio_download_options_json: JsonType) -> None:

        self._log.debug(f'Start [funcName](user_id=\'{user_id}\', video_id=\'{video_id}\')')
        audio_recording = self._user_audio_persistence.get_user_audio_recording_by_video_id(user_id, video_id)

        if audio_recording is not None:

            raise AudioRecordingAlreadyDownloadedException(user_id, video_id)

        else:

            audio_download_options = self._user_audio_adapter.adapt_audio_download_options(audio_download_options_json)
            download_directory = self._user_audio_persistence.get_audio_files_directory_for_user(user_id)
            filename = f'{audio_download_options.artist} - {audio_download_options.title}'
            file, file_size_megabytes = self._youtube_audio_downloader.download_audio(video_id,
                                                                                      download_directory,
                                                                                      filename,
                                                                                      audio_download_options)

            audio_recording = AudioRecording(id_=uuid4(),
                                             video_id=video_id,
                                             user_id=user_id,
                                             file=file,
                                             file_size_megabytes=file_size_megabytes,
                                             title=audio_download_options.title,
                                             artist=audio_download_options.artist,
                                             codec=audio_download_options.codec,
                                             bit_rate=audio_download_options.bit_rate)

            self._user_audio_persistence.save_user_audio_recording(audio_recording)

        self._log.debug(f'End [funcName](user_id=\'{user_id}\', video_id=\'{video_id}\')')

    def get_all_user_audio_recordings(self, user_id: UUID) -> list[OutputAudioRecording]:

        self._log.debug(f'Start [funcName](user_id=\'{user_id}\')')
        audio_recordings = self._user_audio_persistence.get_all_user_audio_recordings(user_id)
        result = self._user_audio_adapter.adapt_output_audio_recordings(audio_recordings)
        self._log.debug(f'End [funcName](user_id=\'{user_id}\')')

        return result

    def delete_user_audio_recording(self, user_id: UUID, recording_id: UUID) -> None:

        self._log.debug(f'Start [funcName](user_id=\'{user_id}\', recording_id=\'{recording_id}\')')
        audio_recording = self._user_audio_persistence.get_audio_recording_by_recording_id(recording_id)

        if audio_recording is not None:

            self._user_audio_persistence.delete_user_audio_recording(audio_recording)

        else:

            raise AudioRecordingNotFoundException(recording_id)

        self._log.debug(f'End [funcName](user_id=\'{user_id}\', recording_id=\'{recording_id}\')')

    def download_user_audio_recording(self, user_id: UUID, recording_id: UUID) -> bytes:

        self._log.debug(f'Start [funcName](user_id=\'{user_id}\', recording_id=\'{recording_id}\')')
        audio_recording = self._user_audio_persistence.get_audio_recording_by_recording_id(recording_id)

        if audio_recording is not None:

            result = self._open_file(audio_recording.file)
            self._log.debug(f'End [funcName](user_id=\'{user_id}\', recording_id=\'{recording_id}\')')

            return result

        else:

            raise AudioRecordingNotFoundException(recording_id)

    @staticmethod
    def _open_file(file_path: str) -> bytes:

        with open(file_path, 'rb') as file:

            return file.read()
