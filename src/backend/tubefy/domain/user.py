from uuid import UUID

from .audio_recording import AudioRecording


class User:

    id: UUID
    username: str
    audio_recordings: list[AudioRecording]

    def __init__(self, id_: UUID, username: str, audio_recordings: list[AudioRecording]):

        self.id = id_
        self.username = username
        self.audio_recordings = audio_recordings

    def __str__(self) -> str:

        return f'{self.__class__.__name__}(id=\'{self.id}\')'
