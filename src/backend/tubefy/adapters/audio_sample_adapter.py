import logging

from logging import Logger
from pathlib import Path
from uuid import UUID

from ..domain.audio_sample import AudioSample
from ..dtos.audio_output import AudioOutput
from ..persistence.domain.database_audio_sample import DatabaseAudioSample


class AudioSampleAdapter:

    _log: Logger = logging.getLogger(__name__)

    def adapt_to_domain(self, database_audio_sample: DatabaseAudioSample) -> AudioSample:

        self._log.debug(f'Start [funcName](database_audio_sample={database_audio_sample})')
        result: AudioSample = AudioSample(
            id_=UUID(database_audio_sample.id),
            video_id=database_audio_sample.video_id,
            file_path=Path(database_audio_sample.file_path)
        )
        self._log.debug(f'End [funcName](database_audio_sample={database_audio_sample})')

        return result

    def adapt_to_output_file(self, audio_sample: AudioSample) -> AudioOutput:

        self._log.debug(f'Start [funcName](audio_sample={audio_sample})')
        result: AudioOutput = AudioOutput(audio_sample.file_path)
        self._log.debug(f'End [funcName](audio_sample={audio_sample})')

        return result

    def adapt_to_persistence(self, audio_sample: AudioSample) -> DatabaseAudioSample:

        self._log.debug(f'Start [funcName](audio_sample={audio_sample})')
        result: DatabaseAudioSample = DatabaseAudioSample(
            id=str(audio_sample.id),
            video_id=audio_sample.video_id,
            file_path=str(audio_sample.file_path)
        )
        self._log.debug(f'End [funcName](audio_sample={audio_sample})')

        return result
