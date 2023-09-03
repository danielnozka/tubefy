import logging
import os

from logging import Logger
from threading import Timer


class SampleAudioCleaner:

    _log: Logger = logging.getLogger(__name__)
    _cleanup_interval_seconds: float = 21600.0
    _timer: Timer
    _sample_files_directory_path: str

    def __init__(self, sample_files_directory_path: str):

        self._sample_files_directory_path = sample_files_directory_path

    def cleanup(self) -> None:

        self._log.debug('Start [funcName]()')

        if os.path.isdir(self._sample_files_directory_path):

            for filename in os.listdir(self._sample_files_directory_path):

                file_path = os.path.join(self._sample_files_directory_path, filename)

                try:

                    os.remove(file_path)

                except Exception as exception:

                    self._log.warning(f'Exception found removing sample file \'{file_path}\'',
                                      extra={'exception': exception})

        self._start_timer()
        self._log.debug('End [funcName]()')

    def _start_timer(self) -> None:

        self._timer = Timer(self._cleanup_interval_seconds, self.cleanup)
        self._timer.start()
