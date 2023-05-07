import os

from datetime import datetime

from youtube_music_manager_server.domain.song import Song
from youtube_music_manager_server.use_cases.music_downloader import MusicDownloader


class MusicDownloaderTest:

    @classmethod
    def test_song_is_downloaded(cls, test_song: Song, music_downloader: MusicDownloader) -> None:

        downloaded_song = music_downloader.download_song(test_song.id, test_song.title, test_song.artist)

        assert isinstance(downloaded_song, Song)
        assert downloaded_song.id == test_song.id
        assert downloaded_song.title == test_song.title
        assert downloaded_song.artist == test_song.artist
        assert isinstance(downloaded_song.creation_date, datetime)
        assert downloaded_song.file == test_song.file
        assert os.path.isfile(downloaded_song.file)
