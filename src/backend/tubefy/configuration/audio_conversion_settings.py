import os

from pathlib import Path


class AudioConversionSettings:

    audio_sample_bit_rate: int
    audio_sample_codec: str
    ffmpeg_location: Path

    def __init__(self, audio_sample_bit_rate: int, audio_sample_codec: str, ffmpeg_location: str):

        self.audio_sample_bit_rate = int(os.environ.get('AUDIO_SAMPLE_BIT_RATE', audio_sample_bit_rate))
        self.audio_sample_codec = os.environ.get('AUDIO_SAMPLE_CODEC', audio_sample_codec)
        self.ffmpeg_location = Path(os.environ.get('FFMPEG_LOCATION', ffmpeg_location))
