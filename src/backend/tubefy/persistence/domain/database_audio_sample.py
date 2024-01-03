from datetime import datetime
from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from .database_model import DatabaseModel


class DatabaseAudioSample(DatabaseModel):

    __tablename__: str = 'audio_samples'

    id: Mapped[str] = mapped_column(String, primary_key=True, unique=True)
    video_id: Mapped[str] = mapped_column(String, unique=True, index=True)
    file_path: Mapped[str] = mapped_column(String)
    creation_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __str__(self) -> str:

        return f'{self.__class__.__name__}(id=\'{self.id}\')'
