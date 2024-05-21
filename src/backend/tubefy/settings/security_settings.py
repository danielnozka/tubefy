from pydantic import Field
from pydantic_settings import BaseSettings


class SecuritySettings(BaseSettings):

    json_web_token_algorithm: str = Field(alias='JSON_WEB_TOKEN_ALGORITHM', default='HS256')
    json_web_token_expiration_minutes: float = Field(alias='JSON_WEB_TOKEN_EXPIRATION_MINUTES', default=60.0)
    json_web_token_key: str = Field(alias='JSON_WEB_TOKEN_KEY')
