from abc import ABC, abstractmethod
from fastapi import APIRouter


class AppBaseController(ABC):

    @property
    @abstractmethod
    def api_router(self) -> APIRouter:

        raise NotImplementedError
