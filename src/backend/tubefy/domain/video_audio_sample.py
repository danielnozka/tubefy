from .base_video_audio import BaseVideoAudio


class VideoAudioSample(BaseVideoAudio):

    def __str__(self) -> str:

        return f'video_audio_sample.video_id=\'{self.video_id}\', video_audio_sample.file_path=\'{self.file_path}\''
