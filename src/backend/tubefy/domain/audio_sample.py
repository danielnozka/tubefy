from pathlib import Path
from uuid import UUID


class AudioSample:

    id: UUID
    video_id: str
    file_path: Path

    def __init__(self, id_: UUID, video_id: str, file_path: Path) -> None:

        self.id = id_
        self.video_id = video_id
        self.file_path = file_path

    def __str__(self) -> str:

        return f'{self.__class__.__name__}(id=\'{self.id}\')'
