import os

from datetime import datetime
from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide

from youtube_music_manager_server.configuration.app_settings import AppSettings
from youtube_music_manager_server.domain.song import Song
from youtube_music_manager_server.dtos.input_song import InputSong
from youtube_music_manager_server.use_cases.music_downloader import MusicDownloader


class MusicDownloaderTest:

    @staticmethod
    @inject
    def test_song_is_downloaded(unit_tests_input_song: InputSong, music_downloader: MusicDownloader,
                                app_settings: AppSettings = Provide['app_settings']) -> None:

        downloaded_song = music_downloader.download_song(unit_tests_input_song)
        music_files_directory = os.path.abspath(app_settings.persistence_settings.music_files_directory)

        assert isinstance(downloaded_song, Song)
        assert downloaded_song.id == unit_tests_input_song.id
        assert downloaded_song.title == unit_tests_input_song.title
        assert downloaded_song.artist == unit_tests_input_song.artist
        assert isinstance(downloaded_song.creation_date, datetime)
        assert os.path.dirname(downloaded_song.file) == music_files_directory
        assert os.path.isfile(downloaded_song.file)
        assert downloaded_song.file_size_megabytes > 0.0
        assert downloaded_song.audio_codec == unit_tests_input_song.audio_codec
        assert downloaded_song.audio_bit_rate == unit_tests_input_song.audio_bit_rate
