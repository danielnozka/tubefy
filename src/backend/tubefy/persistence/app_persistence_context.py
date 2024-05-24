import logging
from aiopath import AsyncPath
from dependency_injector.wiring import inject, Provide
from pathlib import Path
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from uuid import UUID
from .domain.audio_recording_persistence_domain import AudioRecordingPersistenceDomain
from .domain.audio_sample_persistence_domain import AudioSamplePersistenceDomain
from .domain.base_persistence_domain import BasePersistenceDomain
from .domain.user_persistence_domain import UserPersistenceDomain
from ..services.directory_handler import DirectoryHandler
from ..settings.app_settings import AppSettings


logging.getLogger('aiosqlite').propagate = False


class AppPersistenceContext:

    _database_file: str = 'tubefy.db'
    _audio_recordings_directory: str = 'recordings'
    _samples_directory: str = 'samples'
    _audio_recordings_directory_path: Path
    _samples_directory_path: Path
    _directory_handler: DirectoryHandler
    _engine: AsyncEngine
    _session_maker: async_sessionmaker[AsyncSession]

    @inject
    def __init__(
        self,
        directory_handler: DirectoryHandler = Provide['directory_handler'],
        app_settings: AppSettings = Provide['app_settings']
    ) -> None:

        data_path: Path = directory_handler.create_directory(app_settings.persistence_settings.data_path)
        database_path: Path = data_path.joinpath(f'{app_settings.app_name}.db')
        self._audio_recordings_directory_path = directory_handler.create_directory(
            data_path.joinpath(self._audio_recordings_directory)
        )
        self._samples_directory_path = directory_handler.create_directory(data_path.joinpath(self._samples_directory))
        self._directory_handler = directory_handler
        self._engine = create_async_engine(f'sqlite+aiosqlite:///{database_path}')
        self._session_maker = async_sessionmaker(bind=self._engine, expire_on_commit=False)

    async def begin(self) -> None:

        async with self._engine.begin() as connection:

            await connection.run_sync(BasePersistenceDomain.metadata.create_all)

    async def dispose(self) -> None:

        await self._engine.dispose()

    async def get_audio_sample(self, video_id: str) -> AudioSamplePersistenceDomain | None:

        async with self._session_maker() as session:

            return (
                await session.execute(
                    select(AudioSamplePersistenceDomain).where(AudioSamplePersistenceDomain.video_id == video_id)
                )
            ).scalars().first()

    async def add_audio_sample(self, audio_sample: AudioSamplePersistenceDomain) -> None:

        async with self._session_maker() as session:

            async with session.begin():

                session.add(audio_sample)

    async def get_all_audio_samples(self) -> list[AudioSamplePersistenceDomain]:

        async with self._session_maker() as session:

            return list((await session.execute(select(AudioSamplePersistenceDomain))).scalars().all())

    async def delete_all_audio_samples(self) -> None:

        async with self._session_maker() as session:

            audio_samples: list[AudioSamplePersistenceDomain] = list(
                (await session.execute(select(AudioSamplePersistenceDomain))).scalars().all()
            )

        async with self._session_maker() as session:

            async with session.begin():

                audio_sample: AudioSamplePersistenceDomain
                for audio_sample in audio_samples:

                    audio_sample_file_path: AsyncPath = AsyncPath(audio_sample.file_path)

                    if await audio_sample_file_path.is_file():

                        await audio_sample_file_path.unlink()

                    await session.delete(audio_sample)

    async def get_user(self, username: str) -> UserPersistenceDomain | None:

        async with self._session_maker() as session:

            return (
                await session.execute(
                    select(UserPersistenceDomain).where(UserPersistenceDomain.username == username)
                )
            ).scalars().first()

    async def add_user(self, user: UserPersistenceDomain) -> None:

        async with self._session_maker() as session:

            async with session.begin():

                session.add(user)

    async def get_audio_recording(self, audio_recording_id: UUID) -> AudioRecordingPersistenceDomain | None:

        async with self._session_maker() as session:

            return (
                await session.execute(
                    select(AudioRecordingPersistenceDomain).where(
                        AudioRecordingPersistenceDomain.id == str(audio_recording_id)
                    )
                )
            ).scalars().first()

    async def add_audio_recording(self, audio_recording: AudioRecordingPersistenceDomain) -> None:

        async with self._session_maker() as session:

            async with session.begin():

                session.add(audio_recording)

    async def delete_audio_recording(self, audio_recording: AudioRecordingPersistenceDomain) -> None:

        async with self._session_maker() as session:

            async with session.begin():

                audio_recording_file_path: AsyncPath = AsyncPath(audio_recording.file_path)

                if await audio_recording_file_path.is_file():

                    await audio_recording_file_path.unlink()

                await session.delete(audio_recording)

    async def get_user_audio_recordings_directory(self, user_id: UUID) -> Path:

        return await self._directory_handler.create_directory_async(
            self._audio_recordings_directory_path.joinpath(str(user_id))
        )

    @staticmethod
    def get_audio_recording_filename(artist: str, title: str) -> str:

        return f'{artist} - {title}'

    def get_audio_samples_directory(self) -> Path:

        return self._samples_directory_path

    @staticmethod
    def get_audio_sample_filename(video_id: str) -> str:

        return video_id
