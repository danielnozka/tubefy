import logging

from dependency_injector.wiring import inject, Provide
from logging import Logger

from ..adapters.audio_sample_adapter import AudioSampleAdapter
from ..communications.youtube_audio_downloader import YoutubeAudioDownloader
from ..domain.audio_sample import AudioSample
from ..dtos.audio_output import AudioOutput
from ..exceptions.audio_file_not_found_exception import AudioFileNotFoundException
from ..persistence.audio_samples_persistence import AudioSamplesPersistence
from ..persistence.domain.database_audio_sample import DatabaseAudioSample


class AudioSampleGetter:

    _log: Logger = logging.getLogger(__name__)
    _audio_sample_adapter: AudioSampleAdapter
    _youtube_audio_downloader: YoutubeAudioDownloader
    _audio_samples_persistence: AudioSamplesPersistence

    @inject
    def __init__(
        self,
        audio_sample_adapter: AudioSampleAdapter = Provide['audio_sample_adapter'],
        youtube_audio_downloader: YoutubeAudioDownloader = Provide['youtube_audio_downloader'],
        audio_samples_persistence: AudioSamplesPersistence = Provide['audio_samples_persistence']
    ):

        self._audio_sample_adapter = audio_sample_adapter
        self._youtube_audio_downloader = youtube_audio_downloader
        self._audio_samples_persistence = audio_samples_persistence

    def get(self, video_id: str) -> AudioOutput:

        self._log.debug(f'Start [funcName](video_id=\'{video_id}\')')
        database_audio_sample: DatabaseAudioSample | None = self._audio_samples_persistence.get_audio_sample(video_id)

        if database_audio_sample is None:

            audio_sample: AudioSample = self._youtube_audio_downloader.download_audio_sample(
                video_id=video_id,
                output_directory=self._audio_samples_persistence.get_audio_samples_directory(),
                output_filename=self._audio_samples_persistence.get_audio_sample_filename(video_id)
            )
            database_audio_sample: DatabaseAudioSample = self._audio_sample_adapter.adapt_to_persistence(audio_sample)
            self._audio_samples_persistence.add_audio_sample(database_audio_sample)

        else:

            audio_sample: AudioSample = self._audio_sample_adapter.adapt_to_domain(database_audio_sample)

            if not audio_sample.file_path.is_file():

                raise AudioFileNotFoundException(audio_sample.file_path)

        result: AudioOutput = self._audio_sample_adapter.adapt_to_output_file(audio_sample)
        self._log.debug(f'End [funcName](video_id=\'{video_id}\')')

        return result
