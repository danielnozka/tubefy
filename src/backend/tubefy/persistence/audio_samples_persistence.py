import logging
from dependency_injector.wiring import inject, Provide
from logging import Logger
from pathlib import Path
from .app_persistence_context import AppPersistenceContext
from .domain.audio_sample_persistence_domain import AudioSamplePersistenceDomain


class AudioSamplesPersistence:

    _log: Logger = logging.getLogger(__name__)
    _context: AppPersistenceContext

    @inject
    def __init__(self, context: AppPersistenceContext = Provide['app_persistence_context']) -> None:

        self._context = context

    async def get_audio_sample(self, video_id: str) -> AudioSamplePersistenceDomain | None:

        self._log.debug(f'Start [funcName](video_id=\'{video_id}\')')
        result: AudioSamplePersistenceDomain | None = await self._context.get_audio_sample(video_id)
        self._log.debug(f'End [funcName](video_id=\'{video_id}\')')

        return result

    async def add_audio_sample(self, audio_sample: AudioSamplePersistenceDomain) -> None:

        self._log.debug(f'Start [funcName](audio_sample={audio_sample})')
        await self._context.add_audio_sample(audio_sample)
        self._log.debug(f'End [funcName](audio_sample={audio_sample})')

    async def delete_all_audio_samples(self) -> None:

        self._log.debug('Start [funcName]()')
        await self._context.delete_all_audio_samples()
        self._log.debug('End [funcName]()')

    def get_audio_samples_directory(self) -> Path:

        return self._context.get_audio_samples_directory()

    def get_audio_sample_filename(self, video_id: str) -> str:

        return self._context.get_audio_sample_filename(video_id)
