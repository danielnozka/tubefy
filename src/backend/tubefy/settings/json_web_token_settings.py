from pydantic import Field
from pydantic_settings import BaseSettings


class JsonWebTokenSettings(BaseSettings):

    algorithm: str = Field(alias='JSON_WEB_TOKEN_ALGORITHM', default='HS256')
    expiration_minutes: float = Field(alias='JSON_WEB_TOKEN_EXPIRATION_MINUTES', default=60.0)
    key: str = Field(alias='JSON_WEB_TOKEN_KEY')
