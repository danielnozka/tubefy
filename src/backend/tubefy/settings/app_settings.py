from pydantic import Field
from pydantic_settings import BaseSettings
from .audio_conversion_settings import AudioConversionSettings
from .persistence_settings import PersistenceSettings
from .security_settings import SecuritySettings
from .server_settings import ServerSettings


class AppSettings(BaseSettings):

    app_name: str = Field(alias='APP_NAME', default='tubefy')
    audio_conversion_settings: AudioConversionSettings = AudioConversionSettings()
    persistence_settings: PersistenceSettings = PersistenceSettings()
    security_settings: SecuritySettings = SecuritySettings()
    server_settings: ServerSettings = ServerSettings()
