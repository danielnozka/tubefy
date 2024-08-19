from abc import ABC, abstractmethod
from pathlib import Path
from uuid import UUID
from ..domain.audio_download_options import AudioDownloadOptions
from ..domain.user_audio import UserAudio
from ..domain.user import User


class IUserAudioRepository(ABC):

    @abstractmethod
    async def get_user_audio(self, user_audio_id: UUID) -> UserAudio | None:

        raise NotImplementedError

    @abstractmethod
    async def add_user_audio(self, user_audio: UserAudio) -> None:

        raise NotImplementedError

    @abstractmethod
    async def delete_user_audio(self, user_audio: UserAudio) -> None:

        raise NotImplementedError

    @abstractmethod
    def get_user_audio_directory_path(self, user: User) -> Path:

        raise NotImplementedError

    @abstractmethod
    def get_user_audio_filename(self, audio_download_options: AudioDownloadOptions) -> str:

        raise NotImplementedError
