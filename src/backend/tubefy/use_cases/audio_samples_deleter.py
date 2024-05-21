import asyncio
import logging

from dependency_injector.wiring import inject, Provide
from logging import Logger

from ..persistence.audio_samples_persistence import AudioSamplesPersistence
from ..settings.app_settings import AppSettings


class AudioSamplesDeleter:

    _log: Logger = logging.getLogger(__name__)
    _deletion_interval_seconds: float
    _audio_samples_persistence: AudioSamplesPersistence

    @inject
    def __init__(
        self,
        app_settings: AppSettings = Provide['app_settings'],
        audio_samples_persistence: AudioSamplesPersistence = Provide['audio_samples_persistence']
    ) -> None:

        self._deletion_interval_seconds = app_settings.persistence_settings.audio_samples_deletion_interval_hours * 3600
        self._audio_samples_persistence = audio_samples_persistence

    async def delete(self) -> None:

        self._log.debug('Start [funcName]()')
        await self._audio_samples_persistence.delete_all_audio_samples()
        asyncio.get_event_loop().call_later(self._deletion_interval_seconds, asyncio.create_task, self.delete())
        self._log.debug('End [funcName]()')
