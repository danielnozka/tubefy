import logging

from dependency_injector.wiring import inject, Provide
from logging import Logger

from ..adapters.video_audio_adapter import VideoAudioAdapter
from ..communications import YoutubeAudioDownloader
from ..dtos import VideoAudioOutput
from ..persistence import VideoAudioSamplePersistence


class VideoAudioSampleGetter:

    _log: Logger = logging.getLogger(__name__)
    _video_audio_adapter: VideoAudioAdapter
    _youtube_audio_downloader: YoutubeAudioDownloader
    _video_audio_sample_persistence: VideoAudioSamplePersistence

    @inject
    def __init__(
        self,
        video_audio_adapter: VideoAudioAdapter = Provide['video_audio_adapter'],
        youtube_audio_downloader: YoutubeAudioDownloader = Provide['youtube_audio_downloader'],
        video_audio_sample_persistence: VideoAudioSamplePersistence = Provide['video_audio_sample_persistence']
    ):

        self._video_audio_adapter = video_audio_adapter
        self._youtube_audio_downloader = youtube_audio_downloader
        self._video_audio_sample_persistence = video_audio_sample_persistence

    def get(self, video_id: str) -> VideoAudioOutput:

        self._log.debug(f'Start [funcName](video_id=\'{video_id}\')')

        video_audio_sample = self._video_audio_sample_persistence.get_video_audio_sample(video_id)

        if not self._video_audio_sample_persistence.video_audio_sample_exists(video_audio_sample):

            self._youtube_audio_downloader.download(video_audio_sample)

        result = self._video_audio_adapter.adapt(video_audio_sample)

        self._log.debug(f'End [funcName](video_id=\'{video_id}\')')

        return result
