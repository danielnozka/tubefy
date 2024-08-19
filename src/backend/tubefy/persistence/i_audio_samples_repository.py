from abc import ABC, abstractmethod
from pathlib import Path
from ..domain.audio import Audio


class IAudioSamplesRepository(ABC):

    @abstractmethod
    async def get_audio_sample(self, video_id: str) -> Audio | None:

        raise NotImplementedError

    @abstractmethod
    async def add_audio_sample(self, audio_sample: Audio) -> None:

        raise NotImplementedError

    @abstractmethod
    async def delete_all_audio_samples(self) -> None:

        raise NotImplementedError

    @abstractmethod
    def get_audio_samples_directory_path(self) -> Path:

        raise NotImplementedError

    @abstractmethod
    def get_audio_sample_filename(self, video_id: str) -> str:

        raise NotImplementedError
