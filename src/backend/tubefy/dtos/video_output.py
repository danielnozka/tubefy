from humps import camelize
from pydantic import BaseModel


class VideoOutput(BaseModel):

    id: str
    title: str
    thumbnail_url: str

    class Config:

        alias_generator = camelize
        populate_by_name = True
