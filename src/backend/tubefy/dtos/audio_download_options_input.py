from .base_json_dto import BaseJsonDto


class AudioDownloadOptionsInput(BaseJsonDto):

    title: str
    artist: str
    codec: str
    bit_rate: int

    def __str__(self) -> str:

        return (
            f'{self.__class__.__name__}(title=\'{self.title}\', artist=\'{self.artist}\', '
            f'codec=\'{self.codec}\', bit_rate={self.bit_rate})'
        )
