from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings


class YoutubeAudioDownloaderSettings(BaseSettings):

    ffmpeg_path: Path = Field(alias='FFMPEG_PATH')
