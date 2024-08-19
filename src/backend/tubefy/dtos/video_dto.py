from .base_json_dto import BaseJsonDto


class VideoDto(BaseJsonDto):

    id: str
    title: str
    thumbnail_url: str
