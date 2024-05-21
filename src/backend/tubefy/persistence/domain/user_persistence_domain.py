from datetime import datetime
from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from typing import TYPE_CHECKING

from .base_persistence_domain import BasePersistenceDomain


if TYPE_CHECKING:

    from .audio_recording_persistence_domain import AudioRecordingPersistenceDomain


class UserPersistenceDomain(BasePersistenceDomain):

    __tablename__: str = 'users'

    id: Mapped[str] = mapped_column(String, primary_key=True, unique=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    password: Mapped[str] = mapped_column(String)
    creation_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    audio_recordings: Mapped[list['AudioRecordingPersistenceDomain']] = relationship(
        back_populates='user',
        lazy='subquery'
    )

    def __str__(self) -> str:

        return f'{self.__class__.__name__}(id=\'{self.id}\')'
