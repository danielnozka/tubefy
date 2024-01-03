from humps import camelize
from pydantic import BaseModel


class AudioDownloadOptionsInput(BaseModel):

    title: str
    artist: str
    codec: str
    bit_rate: int

    class Config:

        alias_generator = camelize
        populate_by_name = True

    def __str__(self) -> str:

        return f'{self.__class__.__name__}(title=\'{self.title}\', artist=\'{self.artist}\', codec=\'{self.codec}\', ' \
               f'bit_rate={self.bit_rate})'
