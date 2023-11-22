from ..server import BaseDto


class VideoOutput(BaseDto):

    id: str
    title: str
    thumbnail_url: str
