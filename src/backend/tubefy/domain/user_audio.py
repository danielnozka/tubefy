from dataclasses import dataclass, field
from uuid import UUID
from .audio import Audio


@dataclass
class UserAudio(Audio):

    user_id: UUID
    title: str = field(repr=False)
    artist: str = field(repr=False)
