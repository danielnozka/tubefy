class OutputSong:

    def __init__(self, id_: str, title: str, artist: str, file_size_megabytes: float, audio_codec: str,
                 audio_bit_rate: int):

        self.id = id_
        self.title = title
        self.artist = artist
        self.file_size_megabytes = file_size_megabytes
        self.audio_codec = audio_codec
        self.audio_bit_rate = audio_bit_rate
