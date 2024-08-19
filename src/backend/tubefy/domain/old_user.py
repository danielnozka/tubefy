from dataclasses import dataclass, field
from uuid import UUID
from .audio_recording import AudioRecording


@dataclass
class User:

    id: UUID
    username: str = field(repr=False)
    audio_recordings: list[AudioRecording] = field(repr=False)
