from uuid import UUID


class AudioRecording:

    id: UUID
    video_id: str
    user_id: UUID
    title: str
    artist: str
    file: str
    file_size_megabytes: float
    codec: str
    bit_rate: int

    def __init__(self,
                 id_: UUID,
                 video_id: str,
                 user_id: UUID,
                 title: str,
                 artist: str,
                 file: str,
                 file_size_megabytes: float,
                 codec: str,
                 bit_rate: int):

        self.id = id_
        self.video_id = video_id
        self.user_id = user_id
        self.title = title
        self.artist = artist
        self.file = file
        self.file_size_megabytes = file_size_megabytes
        self.codec = codec
        self.bit_rate = bit_rate

    def __str__(self) -> str:

        return f'audio_recording.id=\'{self.id}\''
