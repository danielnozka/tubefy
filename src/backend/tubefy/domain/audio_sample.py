from dataclasses import dataclass, field
from pathlib import Path
from uuid import UUID


@dataclass
class AudioSample:

    id: UUID
    video_id: str = field(repr=False)
    file_path: Path = field(repr=False)
