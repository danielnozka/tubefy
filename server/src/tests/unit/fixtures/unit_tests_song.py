import os
import pytest

from datetime import datetime
from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide

from youtube_music_manager_server.configuration.app_settings import AppSettings
from youtube_music_manager_server.domain.song import Song


@pytest.fixture(scope='package')
@inject
def unit_tests_song(app_settings: AppSettings = Provide['app_settings']) -> Song:

    song_id = 'Ghf8gBEZICc'
    song_title = 'Push it to the limit'
    song_artist = 'Paul Engemann'
    song_creation_date = datetime.now()
    music_files_absolute_directory = os.path.abspath(app_settings.persistence_settings.music_files_directory)
    song_file = os.path.join(music_files_absolute_directory, f'{song_artist} - {song_title}.flac')

    song = Song(id_=song_id,
                title=song_title,
                artist=song_artist,
                creation_date=song_creation_date,
                file=song_file)

    return song
