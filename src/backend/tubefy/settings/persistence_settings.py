from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings


class PersistenceSettings(BaseSettings):

    data_path: Path = Field(alias='DATA_PATH', default='./data')
    audio_samples_deletion_interval_hours: float = Field(alias='AUDIO_SAMPLES_DELETION_INTERVAL_HOURS', default=24.0)
