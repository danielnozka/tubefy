import logging

from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide
from logging import Logger
from uuid import UUID

from ..communications.youtube_audio_downloader import YoutubeAudioDownloader
from ..exceptions.audio_recording_not_found_exception import AudioRecordingNotFoundException
from ..persistence.user_audio_persistence import UserAudioPersistence
from ..persistence.sample_audio_persistence import SampleAudioPersistence


class AudioPlayerService:

    _log: Logger = logging.getLogger(__name__)
    _youtube_audio_downloader: YoutubeAudioDownloader
    _user_audio_persistence: UserAudioPersistence
    _sample_audio_persistence: SampleAudioPersistence

    @inject
    def __init__(self,
                 youtube_audio_downloader: YoutubeAudioDownloader = Provide['youtube_audio_downloader'],
                 user_audio_persistence: UserAudioPersistence = Provide['user_audio_persistence'],
                 sample_audio_persistence: SampleAudioPersistence = Provide['sample_audio_persistence']):

        self._youtube_audio_downloader = youtube_audio_downloader
        self._user_audio_persistence = user_audio_persistence
        self._sample_audio_persistence = sample_audio_persistence

    def play_audio_sample(self, video_id: str) -> bytes:

        self._log.debug(f'Start [funcName](video_id=\'{video_id}\')')
        sample_audio_file = self._sample_audio_persistence.get_sample_audio_file(video_id)

        if sample_audio_file is None:

            sample_files_directory = self._sample_audio_persistence.get_sample_files_directory()
            filename = video_id
            sample_audio_file, _ = self._youtube_audio_downloader.download_audio(video_id,
                                                                                 sample_files_directory,
                                                                                 filename)

        result = self._open_file(sample_audio_file)
        self._log.debug(f'End [funcName](video_id=\'{video_id}\')')

        return result

    def play_user_saved_audio(self, user_id: UUID, recording_id: UUID) -> bytes:

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
