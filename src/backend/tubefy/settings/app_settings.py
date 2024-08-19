from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):

    host: str = Field(alias='APP_HOST', default='0.0.0.0')
    port: int = Field(alias='APP_PORT', default=9000)
    frontend_directory_path: Path = Field(alias='APP_FRONTEND_DIRECTORY_PATH', default='./static/browser')
