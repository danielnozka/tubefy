from humps import camelize
from pydantic import BaseModel


class BaseJsonDto(BaseModel):

    class Config:

        alias_generator = camelize
        populate_by_name = True

    def __str__(self) -> str:

        return self.__repr__()
