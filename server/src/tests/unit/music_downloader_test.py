import os

from datetime import datetime
from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide

from youtube_music_manager_server.configuration import AppSettings
from youtube_music_manager_server.domain import Song
from youtube_music_manager_server.dtos import SongDto
from youtube_music_manager_server.use_cases import MusicDownloader


class MusicDownloaderTest:

    @staticmethod
    @inject
    def test_song_is_downloaded(test_song_dto: SongDto, music_downloader: MusicDownloader,
                                app_settings: AppSettings = Provide['app_settings']) -> None:

        downloaded_song = music_downloader.download_song(test_song_dto)
        music_files_directory = os.path.abspath(app_settings.persistence_settings.music_files_directory)

        assert isinstance(downloaded_song, Song)
        assert downloaded_song.id == test_song_dto.id
        assert downloaded_song.title == test_song_dto.title
        assert downloaded_song.artist == test_song_dto.artist
        assert isinstance(downloaded_song.creation_date, datetime)
        assert os.path.dirname(downloaded_song.file) == music_files_directory
        assert os.path.isfile(downloaded_song.file)
