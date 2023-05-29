class AudioRecording:

    def __init__(self,
                 id_: str,
                 title: str,
                 artist: str,
                 file: str,
                 file_size_megabytes: float,
                 codec: str,
                 bit_rate: int):

        self.id = id_
        self.title = title
        self.artist = artist
        self.file = file
        self.file_size_megabytes = file_size_megabytes
        self.codec = codec
        self.bit_rate = bit_rate

    def __str__(self):

        return f"audio_recording_id='{self.id}'"
