import logging

from dependency_injector.wiring import inject, Provide
from logging import Logger
from threading import Timer

from ..configuration import AppSettings
from ..persistence import AudioSamplesPersistence


class AudioSamplesDeleter:

    _log: Logger = logging.getLogger(__name__)
    _deletion_interval_seconds: float
    _audio_samples_persistence: AudioSamplesPersistence
    _timer: Timer

    @inject
    def __init__(
        self,
        app_settings: AppSettings = Provide['app_settings'],
        audio_samples_persistence: AudioSamplesPersistence = Provide['audio_samples_persistence']
    ):

        self._deletion_interval_seconds = app_settings.persistence_settings.audio_samples_deletion_interval_hours * 3600
        self._audio_samples_persistence = audio_samples_persistence

    def delete(self) -> None:

        self._log.debug('Start [funcName]()')
        self._audio_samples_persistence.delete_all_audio_samples()
        self._schedule_next_deletion()
        self._log.debug('End [funcName]()')

    def _schedule_next_deletion(self) -> None:

        self._timer = Timer(interval=self._deletion_interval_seconds, function=self.delete)
        self._timer.start()
