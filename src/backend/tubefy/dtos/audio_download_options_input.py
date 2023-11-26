class AudioDownloadOptions:

    title: str
    artist: str
    codec: str
    bit_rate: int

    def __init__(self,
                 title: str,
                 artist: str,
                 codec: str,
                 bit_rate: int):

        self.title = title
        self.artist = artist
        self.codec = codec
        self.bit_rate = bit_rate

    def __str__(self) -> str:

        return (f'audio_download_options.title=\'{self.title}\', '
                f'audio_download_options.artist=\'{self.artist}\', '
                f'audio_download_options.codec=\'{self.codec}\', '
                f'audio_download_options.bit_rate={self.bit_rate}')
