import os

from pathlib import Path


class AudioConversionSettings:

    default_bit_rate: int
    default_codec: str
    ffmpeg_location: Path

    def __init__(
        self,
        default_bit_rate: int,
        default_codec: str,
        ffmpeg_location: str
    ):

        self.default_bit_rate = int(os.environ.get('DEFAULT_BIT_RATE', default_bit_rate))
        self.default_codec = os.environ.get('DEFAULT_CODEC', default_codec)
        self.ffmpeg_location = Path(os.environ.get('FFMPEG_LOCATION', ffmpeg_location))
