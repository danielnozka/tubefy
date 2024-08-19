from dataclasses import dataclass, field
from uuid import UUID
from .audio import Audio


@dataclass
class User:

    id: UUID
    username: str = field(repr=False)
    audio_list: list[Audio] = field(repr=False)
