from dataclasses import dataclass, field


@dataclass
class Video:

    id: str
    title: str = field(repr=False)
    thumbnail_url: str = field(repr=False)
