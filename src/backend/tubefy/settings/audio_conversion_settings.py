from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings


class AudioConversionSettings(BaseSettings):

    audio_sample_bit_rate: int = Field(alias='AUDIO_SAMPLE_BIT_RATE', default=96)
    audio_sample_codec: str = Field(alias='AUDIO_SAMPLE_CODEC', default='mp3')
    ffmpeg_location: Path = Field(alias='FFMPEG_LOCATION')
