from abc import ABC, abstractmethod
from ..domain.video import Video


class IVideosRepository(ABC):

    @abstractmethod
    async def search_videos(self, search_query: str) -> list[Video]:

        raise NotImplementedError
