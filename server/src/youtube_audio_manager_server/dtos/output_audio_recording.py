class OutputAudioRecording:

    video_id: str
    title: str
    artist: str
    file_size_megabytes: float
    codec: str
    bit_rate: int

    def __init__(self,
                 video_id: str,
                 title: str,
                 artist: str,
                 file_size_megabytes: float,
                 codec: str,
                 bit_rate: int):

        self.video_id = video_id
        self.title = title
        self.artist = artist
        self.file_size_megabytes = file_size_megabytes
        self.codec = codec
        self.bit_rate = bit_rate
