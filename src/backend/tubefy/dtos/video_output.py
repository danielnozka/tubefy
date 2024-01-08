from .base_json_dto import BaseJsonDto


class VideoOutput(BaseJsonDto):

    id: str
    title: str
    thumbnail_url: str
