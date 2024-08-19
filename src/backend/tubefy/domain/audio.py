from dataclasses import dataclass, field
from pathlib import Path
from uuid import UUID
from .codec import Codec


@dataclass
class Audio:

    id: UUID
    video_id: str
    file_path: Path = field(repr=False)
    codec: Codec = field(repr=False)
    bit_rate: int = field(repr=False)
