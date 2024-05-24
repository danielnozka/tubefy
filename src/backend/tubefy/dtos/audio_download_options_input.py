from .base_json_dto import BaseJsonDto


class AudioDownloadOptionsInput(BaseJsonDto):

    title: str
    artist: str
    codec: str
    bit_rate: int
