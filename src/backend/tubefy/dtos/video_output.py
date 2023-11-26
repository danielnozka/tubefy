from ..server import BaseOutputDto


class VideoOutput(BaseOutputDto):

    id: str
    title: str
    thumbnail_url: str
