import logging

from ..domain.audio_recording import AudioRecording
from ..dtos.input_audio_recording import InputAudioRecording
from ..dtos.output_audio_recording import OutputAudioRecording
from ..tools.typing import JsonType


class AudioAdapter:

    _log = logging.getLogger(__name__)

    def adapt_input(self, audio_recording_id: str, input_data: JsonType) -> InputAudioRecording:

        self._log.debug(f'Start [funcName](audio_recording_id=\'{audio_recording_id}\')')

        input_audio_recording = InputAudioRecording(id_=audio_recording_id,
                                                    title=input_data['title'],
                                                    artist=input_data['artist'],
                                                    codec=input_data['codec'].lower(),
                                                    bit_rate=int(input_data['bitRate']))

        self._log.debug(f'End [funcName](audio_recording_id=\'{audio_recording_id}\')')

        return input_audio_recording

    def adapt_output(self, audio_recordings: list[AudioRecording]) -> list[OutputAudioRecording]:

        self._log.debug('Start [funcName]()')

        result = []

        for audio_recording in audio_recordings:

            output_audio_recording = OutputAudioRecording(id_=audio_recording.id,
                                                          title=audio_recording.title,
                                                          artist=audio_recording.artist,
                                                          file_size_megabytes=audio_recording.file_size_megabytes,
                                                          codec=audio_recording.codec.upper(),
                                                          bit_rate=audio_recording.bit_rate)

            result.append(output_audio_recording)

        self._log.debug('End [funcName]()')

        return result
