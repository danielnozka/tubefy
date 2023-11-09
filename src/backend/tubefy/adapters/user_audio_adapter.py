import logging

from logging import Logger

from ..domain.audio_download_options import AudioDownloadOptions
from ..domain.audio_recording import AudioRecording
from ..dtos.output_audio_recording import OutputAudioRecording
from ..tools.typing import JsonType


class UserAudioAdapter:

    _log: Logger = logging.getLogger(__name__)

    def adapt_audio_download_options(self, audio_download_options_json: JsonType) -> AudioDownloadOptions:

        self._log.debug('Start [funcName]()')

        audio_download_options = AudioDownloadOptions(title=audio_download_options_json['title'],
                                                      artist=audio_download_options_json['artist'],
                                                      codec=audio_download_options_json['codec'].lower(),
                                                      bit_rate=int(audio_download_options_json['bitRate']))

        self._log.debug('End [funcName]()')

        return audio_download_options

    def adapt_output_audio_recordings(self, audio_recordings: list[AudioRecording]) -> list[OutputAudioRecording]:

        self._log.debug('Start [funcName]()')

        result: list[OutputAudioRecording] = []

        for audio_recording in audio_recordings:

            output_audio_recording = OutputAudioRecording(id_=audio_recording.id,
                                                          video_id=audio_recording.video_id,
                                                          title=audio_recording.title,
                                                          artist=audio_recording.artist,
                                                          file_size_megabytes=audio_recording.file_size_megabytes,
                                                          codec=audio_recording.codec.upper(),
                                                          bit_rate=audio_recording.bit_rate)

            result.append(output_audio_recording)

        self._log.debug('End [funcName]()')

        return result
