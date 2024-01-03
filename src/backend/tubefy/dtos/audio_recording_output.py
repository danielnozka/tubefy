from humps import camelize
from pydantic import BaseModel
from uuid import UUID


class AudioRecordingOutput(BaseModel):

    id: UUID
    video_id: str
    title: str
    artist: str
    codec: str
    bit_rate: int

    class Config:

        alias_generator = camelize
        populate_by_name = True
