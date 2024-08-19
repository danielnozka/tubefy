from pydantic import Field
from pydantic_settings import BaseSettings


class AudioDownloaderSettings(BaseSettings):

    default_bit_rate: int = Field(alias='AUDIO_DOWNLOADER_DEFAULT_BIT_RATE', default=96)
    default_codec: str = Field(alias='AUDIO_DOWNLOADER_DEFAULT_CODEC', default='mp3')
