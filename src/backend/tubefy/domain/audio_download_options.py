from dataclasses import dataclass, field
from pathlib import Path
from .codec import Codec


@dataclass
class AudioDownloadOptions:

    video_id: str
    download_directory_path: Path = field(repr=False)
    filename: str = field(repr=False)
    codec: Codec = field(repr=False)
    bit_rate: int = field(repr=False)
    artist: str | None = field(default=None, repr=False)
    title: str | None = field(default=None, repr=False)
    include_thumbnail: bool = field(default=False, repr=False)
