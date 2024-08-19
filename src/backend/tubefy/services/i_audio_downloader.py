from abc import ABC, abstractmethod
from ..domain.audio import Audio
from ..domain.audio_download_options import AudioDownloadOptions


class IAudioDownloader(ABC):

    @abstractmethod
    async def download_audio(self, audio_download_options: AudioDownloadOptions) -> Audio:

        raise NotImplementedError
