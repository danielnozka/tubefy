from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings


class ServerSettings(BaseSettings):

    frontend_build_path: Path = Field(alias='FRONTEND_BUILD_PATH', default='./static/browser')
    host: str = Field(alias='HOST', default='0.0.0.0')
    port: int = Field(alias='PORT', default=9000)
