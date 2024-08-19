from enum import Enum
from ..exceptions.unsupported_codec_exception import UnsupportedCodecException


class Codec(Enum):

    mp3 = 'mp3'
    flac = 'flac'

    @classmethod
    def _missing_(cls, value: str) -> None:

        raise UnsupportedCodecException(value)
