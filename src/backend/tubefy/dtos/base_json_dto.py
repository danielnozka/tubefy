from humps import camelize
from pydantic import BaseModel


class BaseJsonDto(BaseModel):

    class Config:

        alias_generator = camelize
        populate_by_name = True
