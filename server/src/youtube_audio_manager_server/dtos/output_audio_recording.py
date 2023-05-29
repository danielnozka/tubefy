class OutputAudioRecording:

    def __init__(self, id_: str, title: str, artist: str, file_size_megabytes: float, codec: str, bit_rate: int):

        self.id = id_
        self.title = title
        self.artist = artist
        self.file_size_megabytes = file_size_megabytes
        self.codec = codec
        self.bit_rate = bit_rate
