import logging
import os
import requests

from dependency_injector.wiring import inject
from dependency_injector.wiring import Provide
from requests import Response
from string import Template

from youtube_audio_manager_server.configuration.app_settings import AppSettings
from youtube_audio_manager_server.domain.audio_recording import AudioRecording


logging.getLogger('urllib3').propagate = False


class UserAudioServiceTest:

    _end_point_base: Template = Template('/users/${user_id}/audio')
    _end_point_with_video: Template = Template(_end_point_base.template + '/${video_id}')

    @classmethod
    def test_audio_recording_is_downloaded(cls, test_audio_recording: AudioRecording,
                                           test_input_audio_recording_options: dict) -> None:

        response = cls._request_audio_recording_to_be_downloaded(test_audio_recording,
                                                                 test_input_audio_recording_options)

        assert response.status_code == 200
        assert os.path.isfile(test_audio_recording.file)
        assert os.stat(test_audio_recording.file).st_size / (1024 ** 2) > 0.0

        test_file_name, test_file_extension = os.path.splitext(os.path.basename(test_audio_recording.file))

        assert test_file_name == f'{test_audio_recording.artist} - {test_audio_recording.title}'
        assert test_file_extension == f'.{test_audio_recording.codec}'

    @classmethod
    def test_downloading_the_same_audio_recording_twice_raises_exception(cls, test_audio_recording: AudioRecording,
                                                                         test_input_audio_recording_options: dict) -> \
            None:

        response = cls._request_audio_recording_to_be_downloaded(test_audio_recording,
                                                                 test_input_audio_recording_options)

        assert response.status_code == 409

    @classmethod
    def test_audio_recording_is_returned(cls, test_audio_recording: AudioRecording) -> None:

        response = cls._request_audio_recordings_to_be_returned(test_audio_recording)

        assert response.status_code == 200

        json_response = response.json()

        assert type(json_response) == list
        assert len(json_response) == 1

        output_audio_recording = json_response[0]

        assert type(output_audio_recording) == dict
        assert output_audio_recording.get('videoId') == test_audio_recording.video_id
        assert output_audio_recording.get('title') == test_audio_recording.title
        assert output_audio_recording.get('artist') == test_audio_recording.artist
        assert output_audio_recording.get('fileSizeMegabytes') >= test_audio_recording.file_size_megabytes
        assert output_audio_recording.get('codec').lower() == test_audio_recording.codec
        assert output_audio_recording.get('bitRate') == test_audio_recording.bit_rate

    @classmethod
    def test_audio_recording_is_deleted(cls, test_audio_recording: AudioRecording) -> None:

        response = cls._request_audio_recording_to_be_deleted(test_audio_recording)

        assert response.status_code == 200
        assert not os.path.isfile(test_audio_recording.file)

    @classmethod
    def test_no_audio_recordings_are_returned(cls, test_audio_recording: AudioRecording) -> None:

        response = cls._request_audio_recordings_to_be_returned(test_audio_recording)

        assert response.status_code == 200

        json_response = response.json()

        assert type(json_response) == list
        assert len(json_response) == 0

    @classmethod
    def test_deleting_the_same_audio_recording_twice_raises_exception(cls,
                                                                      test_audio_recording: AudioRecording) -> None:

        response = cls._request_audio_recording_to_be_deleted(test_audio_recording)

        assert response.status_code == 404

    @classmethod
    @inject
    def _request_audio_recording_to_be_downloaded(cls, test_audio_recording: AudioRecording,
                                                  test_input_audio_recording_options: dict,
                                                  app_settings: AppSettings = Provide['app_settings']) -> Response:

        end_point = cls._end_point_with_video.substitute(user_id=test_audio_recording.user_id,
                                                         video_id=test_audio_recording.video_id)
        url = f'http://localhost:{app_settings.server_settings.port}' + end_point
        response = requests.put(url, json=test_input_audio_recording_options)

        return response

    @classmethod
    @inject
    def _request_audio_recordings_to_be_returned(cls, test_audio_recording: AudioRecording,
                                                 app_settings: AppSettings = Provide['app_settings']) -> Response:

        end_point = cls._end_point_base.substitute(user_id=test_audio_recording.user_id)
        url = f'http://localhost:{app_settings.server_settings.port}' + end_point
        response = requests.get(url)

        return response

    @classmethod
    @inject
    def _request_audio_recording_to_be_deleted(cls, test_audio_recording: AudioRecording,
                                               app_settings: AppSettings = Provide['app_settings']) -> Response:

        end_point = cls._end_point_with_video.substitute(user_id=test_audio_recording.user_id,
                                                         video_id=test_audio_recording.video_id)
        url = f'http://localhost:{app_settings.server_settings.port}' + end_point
        response = requests.delete(url)

        return response
