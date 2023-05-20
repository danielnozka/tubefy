import logging
import os
import requests

from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide
from requests import Response

from youtube_music_manager_server.configuration.app_settings import AppSettings
from youtube_music_manager_server.domain.song import Song


logging.getLogger('urllib3').propagate = False
logging.getLogger('urllib3').disabled = True


class MusicServiceTest:

    @classmethod
    def test_song_is_downloaded(cls, integration_tests_song: Song, integration_tests_song_input_data: dict) -> None:

        response = cls._request_song_to_be_added(integration_tests_song, integration_tests_song_input_data)

        assert response.status_code == 200
        assert os.path.isfile(integration_tests_song.file)

    @classmethod
    def test_adding_the_same_song_twice_raises_exception(cls, integration_tests_song: Song,
                                                         integration_tests_song_input_data: dict) -> None:

        response = cls._request_song_to_be_added(integration_tests_song, integration_tests_song_input_data)

        assert response.status_code == 409

    @classmethod
    def test_song_is_returned(cls, integration_tests_song: Song, integration_tests_song_input_data: dict) -> None:

        response = cls._request_song_to_be_returned()

        assert response.status_code == 200

        json_response = response.json()

        assert type(json_response) == list
        assert len(json_response) == 1

        output_song = json_response[0]

        assert type(output_song) == dict
        assert output_song.get('id') == integration_tests_song.id
        assert output_song.get('title') == integration_tests_song.title
        assert output_song.get('artist') == integration_tests_song.artist
        assert output_song.get('fileSizeMegabytes') >= integration_tests_song.file_size_megabytes
        assert output_song.get('audioCodec').lower() == integration_tests_song.audio_codec
        assert output_song.get('audioBitRate') == integration_tests_song.audio_bit_rate

    @classmethod
    def test_song_is_deleted(cls, integration_tests_song: Song) -> None:

        response = cls._request_song_to_be_deleted(integration_tests_song)

        assert response.status_code == 200
        assert not os.path.isfile(integration_tests_song.file)

    @classmethod
    def test_no_songs_are_returned(cls) -> None:

        response = cls._request_song_to_be_returned()

        assert response.status_code == 200

        json_response = response.json()

        assert type(json_response) == list
        assert len(json_response) == 0

    @classmethod
    def test_deleting_the_same_song_twice_raises_exception(cls, integration_tests_song: Song) -> None:

        response = cls._request_song_to_be_deleted(integration_tests_song)

        assert response.status_code == 404

    @staticmethod
    @inject
    def _request_song_to_be_added(integration_tests_song: Song, integration_tests_song_input_data: dict,
                                  app_settings: AppSettings = Provide['app_settings']) -> Response:

        url = f'http://localhost:{app_settings.server_settings.port}/music/{integration_tests_song.id}'
        response = requests.put(url, json=integration_tests_song_input_data)

        return response

    @staticmethod
    @inject
    def _request_song_to_be_returned(app_settings: AppSettings = Provide['app_settings']) -> Response:

        url = f'http://localhost:{app_settings.server_settings.port}/music/'
        response = requests.get(url)

        return response

    @staticmethod
    @inject
    def _request_song_to_be_deleted(integration_tests_song: Song,
                                    app_settings: AppSettings = Provide['app_settings']) -> Response:

        url = f'http://localhost:{app_settings.server_settings.port}/music/{integration_tests_song.id}'
        response = requests.delete(url)

        return response
