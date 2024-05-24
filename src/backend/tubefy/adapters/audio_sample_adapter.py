import logging
from logging import Logger
from pathlib import Path
from uuid import UUID
from ..domain.audio_sample import AudioSample
from ..dtos.audio_output import AudioOutput
from ..persistence.domain.audio_sample_persistence_domain import AudioSamplePersistenceDomain


class AudioSampleAdapter:

    _log: Logger = logging.getLogger(__name__)

    def adapt_from_persistence(self, audio_sample: AudioSamplePersistenceDomain) -> AudioSample:

        self._log.debug(f'Start [funcName](audio_sample={audio_sample})')
        result: AudioSample = AudioSample(
            id=UUID(audio_sample.id),
            video_id=audio_sample.video_id,
            file_path=Path(audio_sample.file_path)
        )
        self._log.debug(f'End [funcName](audio_sample={audio_sample})')

        return result

    def adapt_to_output_file(self, audio_sample: AudioSample) -> AudioOutput:

        self._log.debug(f'Start [funcName](audio_sample={audio_sample})')
        result: AudioOutput = AudioOutput(audio_sample.file_path)
        self._log.debug(f'End [funcName](audio_sample={audio_sample})')

        return result

    def adapt_to_persistence(self, audio_sample: AudioSample) -> AudioSamplePersistenceDomain:

        self._log.debug(f'Start [funcName](audio_sample={audio_sample})')
        result: AudioSamplePersistenceDomain = AudioSamplePersistenceDomain(
            id=str(audio_sample.id),
            video_id=audio_sample.video_id,
            file_path=str(audio_sample.file_path)
        )
        self._log.debug(f'End [funcName](audio_sample={audio_sample})')

        return result
