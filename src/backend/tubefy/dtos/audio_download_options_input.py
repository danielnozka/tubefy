from ..server import BaseInputDto


class AudioDownloadOptionsInput(BaseInputDto):

    title: str
    artist: str
    codec: str
    bit_rate: int

    def __str__(self) -> str:

        return (f'audio_download_options_input.title=\'{self.title}\', '
                f'audio_download_options_input.artist=\'{self.artist}\', '
                f'audio_download_options_input.codec=\'{self.codec}\', '
                f'audio_download_options_input.bit_rate={self.bit_rate}')
