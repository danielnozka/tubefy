import logging
from logging import Logger
from ..domain.audio import Audio
from ..domain.audio_download_options import AudioDownloadOptions
from ..domain.codec import Codec
from ..exceptions.audio_file_not_found_exception import AudioFileNotFoundException
from ..persistence.i_audio_samples_repository import IAudioSamplesRepository
from ..services.i_audio_downloader import IAudioDownloader
from ..settings.audio_downloader_settings import AudioDownloaderSettings


class AudioSampleGetter:

    _log: Logger = logging.getLogger(__name__)
    _audio_downloader: IAudioDownloader
    _audio_samples_repository: IAudioSamplesRepository

    def __init__(self, audio_downloader: IAudioDownloader, audio_samples_repository: IAudioSamplesRepository) -> None:

        self._audio_downloader = audio_downloader
        self._audio_samples_repository = audio_samples_repository

    async def get_audio_sample(self, video_id: str) -> Audio:

        self._log.debug(f'Start [funcName](video_id=\'{video_id}\')')
        audio_sample: Audio | None = await self._audio_samples_repository.get_audio_sample(video_id)

        if audio_sample is None:

            settings: AudioDownloaderSettings = AudioDownloaderSettings()
            audio_download_options: AudioDownloadOptions = AudioDownloadOptions(
                video_id=video_id,
                download_directory_path=self._audio_samples_repository.get_audio_samples_directory_path(),
                filename=self._audio_samples_repository.get_audio_sample_filename(video_id),
                codec=Codec(settings.default_codec),
                bit_rate=settings.default_bit_rate
            )
            audio_sample: Audio = await self._audio_downloader.download_audio(audio_download_options)
            await self._audio_samples_repository.add_audio_sample(audio_sample)

        if audio_sample.file_path.is_file():

            self._log.debug(f'End [funcName](video_id=\'{video_id}\')')

            return audio_sample

        raise AudioFileNotFoundException(audio_sample.file_path)
