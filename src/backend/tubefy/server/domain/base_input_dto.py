from humps import decamelize
from pydantic import BaseModel


class BaseInputDto(BaseModel):

    class Config:

        alias_generator = decamelize
        populate_by_name = True
