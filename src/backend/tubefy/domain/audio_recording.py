from pathlib import Path
from uuid import UUID


class AudioRecording:

    id: UUID
    video_id: str
    file_path: Path
    title: str
    artist: str
    codec: str
    bit_rate: int
    user_id: UUID

    def __init__(self,
        id_: UUID,
        video_id: str,
        file_path: Path,
        title: str,
        artist: str,
        codec: str,
        bit_rate: int,
        user_id: UUID
    ) -> None:

        self.id = id_
        self.video_id = video_id
        self.file_path = file_path
        self.title = title
        self.artist = artist
        self.codec = codec
        self.bit_rate = bit_rate
        self.user_id = user_id

    def __str__(self) -> str:

        return f'{self.__class__.__name__}(id=\'{self.id}\')'
