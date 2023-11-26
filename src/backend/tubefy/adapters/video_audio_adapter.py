import logging

from logging import Logger

from ..domain import BaseVideoAudio
from ..dtos import VideoAudioOutput


class VideoAudioAdapter:

    _log: Logger = logging.getLogger(__name__)

    def adapt(self, video_audio: BaseVideoAudio) -> VideoAudioOutput:

        self._log.debug(f'Start [funcName]({video_audio})')
        result = VideoAudioOutput(video_audio.file_path)
        self._log.debug(f'End [funcName]({video_audio})')

        return result
