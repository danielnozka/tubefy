from pathlib import Path


class BaseVideoAudio:

    video_id: str
    file_path: Path

    def __init__(self, video_id: str, file_path: Path):

        self.video_id = video_id
        self.file_path = file_path
