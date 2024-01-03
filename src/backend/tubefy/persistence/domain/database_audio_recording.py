from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from typing import TYPE_CHECKING

from .database_model import DatabaseModel


if TYPE_CHECKING:

    from .database_user import DatabaseUser


class DatabaseAudioRecording(DatabaseModel):

    __tablename__: str = 'audio_recordings'

    id: Mapped[str] = mapped_column(String, primary_key=True, unique=True, index=True)
    video_id: Mapped[str] = mapped_column(String)
    file_path: Mapped[str] = mapped_column(String)
    title: Mapped[str] = mapped_column(String)
    artist: Mapped[str] = mapped_column(String)
    codec: Mapped[str] = mapped_column(String)
    bit_rate: Mapped[int] = mapped_column(Integer)
    user_id: Mapped[str] = mapped_column(ForeignKey('users.id'))
    creation_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped['DatabaseUser'] = relationship(back_populates='audio_recordings', lazy='subquery')

    def __str__(self) -> str:

        return f'{self.__class__.__name__}(id=\'{self.id}\')'
