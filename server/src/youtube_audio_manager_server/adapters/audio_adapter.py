import logging

from logging import Logger

from ..domain.audio_download_options import AudioDownloadOptions
from ..domain.audio_recording import AudioRecording
from ..dtos.output_audio_recording import OutputAudioRecording
from ..tools.typing import JsonType


class AudioAdapter:

    _log: Logger = logging.getLogger(__name__)

    def adapt_input(self, input_data: JsonType) -> AudioDownloadOptions:

        self._log.debug('Start [funcName]()')

        audio_download_options = AudioDownloadOptions(title=input_data['title'],
                                                      artist=input_data['artist'],
                                                      codec=input_data['codec'].lower(),
                                                      bit_rate=int(input_data['bitRate']))

        self._log.debug('End [funcName]()')

        return audio_download_options

    def adapt_output(self, audio_recordings: list[AudioRecording]) -> list[OutputAudioRecording]:

        self._log.debug('Start [funcName]()')

        result: list[OutputAudioRecording] = []

        for audio_recording in audio_recordings:

            output_audio_recording = OutputAudioRecording(video_id=audio_recording.video_id,
                                                          title=audio_recording.title,
                                                          artist=audio_recording.artist,
                                                          file_size_megabytes=audio_recording.file_size_megabytes,
                                                          codec=audio_recording.codec.upper(),
                                                          bit_rate=audio_recording.bit_rate)

            result.append(output_audio_recording)

        self._log.debug('End [funcName]()')

        return result
