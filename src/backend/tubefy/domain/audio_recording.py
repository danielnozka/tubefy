from dataclasses import dataclass, field
from pathlib import Path
from uuid import UUID


@dataclass
class AudioRecording:

    id: UUID
    video_id: str = field(repr=False)
    file_path: Path = field(repr=False)
    title: str = field(repr=False)
    artist: str = field(repr=False)
    codec: str = field(repr=False)
    bit_rate: int = field(repr=False)
    user_id: UUID = field(repr=False)
