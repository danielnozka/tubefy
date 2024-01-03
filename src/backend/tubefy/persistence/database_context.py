from contextlib import contextmanager
from pathlib import Path
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session, sessionmaker
from uuid import UUID

from .domain import DatabaseAudioRecording, DatabaseAudioSample, DatabaseModel, DatabaseUser


class DatabaseContext:

    _database: str = 'tubefy.db'
    _engine: Engine
    _session_maker: sessionmaker

    def __init__(self, database_directory_path: Path):

        self._engine = create_engine(
            url=f'sqlite:///{database_directory_path.joinpath(self._database)}',
            connect_args={
                'check_same_thread': False
            }
        )
        self._session_maker = sessionmaker(autocommit=False, autoflush=False, bind=self._engine)
        DatabaseModel.metadata.create_all(bind=self._engine)

    def close(self) -> None:

        self._engine.dispose()

    def get_audio_sample(self, video_id: str) -> DatabaseAudioSample | None:

        with self._make_session() as session:

            return session.query(DatabaseAudioSample).filter(DatabaseAudioSample.video_id == video_id).first()

    def add_audio_sample(self, database_audio_sample: DatabaseAudioSample) -> None:

        with self._make_session() as session:

            session.add(database_audio_sample)
            session.commit()
            session.refresh(database_audio_sample)

    def get_user(self, username: str) -> DatabaseUser | None:

        with self._make_session() as session:

            return session.query(DatabaseUser).filter(DatabaseUser.username == username).first()

    def add_user(self, database_user: DatabaseUser) -> None:

        with self._make_session() as session:

            session.add(database_user)
            session.commit()
            session.refresh(database_user)

    def get_audio_recording(self, audio_recording_id: UUID) -> DatabaseAudioRecording | None:

        with self._make_session() as session:

            return session.query(DatabaseAudioRecording).filter(
                DatabaseAudioRecording.id == str(audio_recording_id)
            ).first()

    def add_audio_recording(self, database_audio_recording: DatabaseAudioRecording) -> None:

        with self._make_session() as session:

            session.add(database_audio_recording)
            session.commit()
            session.refresh(database_audio_recording)

    def delete_audio_recording(self, database_audio_recording: DatabaseAudioRecording) -> None:

        with self._make_session() as session:

            session.delete(database_audio_recording)
            session.commit()

    @contextmanager
    def _make_session(self) -> Session:

        session = self._session_maker()

        try:

            yield session

        finally:

            session.close()
