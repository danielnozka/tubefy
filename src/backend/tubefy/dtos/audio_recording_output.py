from uuid import UUID

from .base_json_dto import BaseJsonDto


class AudioRecordingOutput(BaseJsonDto):

    id: UUID
    video_id: str
    title: str
    artist: str
    codec: str
    bit_rate: int
