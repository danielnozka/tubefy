import logging
from logging import Logger
from pathlib import Path
from uuid import UUID
from ..domain.audio_recording import AudioRecording
from ..domain.old_user import User
from ..dtos.audio_recording_output import AudioRecordingOutput
from ..dtos.audio_output import AudioOutput
from ..persistence.domain.audio_recording_persistence_domain import AudioRecordingPersistenceDomain


class AudioRecordingAdapter:

    _log: Logger = logging.getLogger(__name__)

    def adapt_from_persistence(self, audio_recording: AudioRecordingPersistenceDomain) -> AudioRecording:

        self._log.debug(f'Start [funcName](audio_recording={audio_recording})')
        result: AudioRecording = AudioRecording(
            id=UUID(audio_recording.id),
            video_id=audio_recording.video_id,
            file_path=Path(audio_recording.file_path),
            title=audio_recording.title,
            artist=audio_recording.artist,
            codec=audio_recording.codec,
            bit_rate=audio_recording.bit_rate,
            user_id=UUID(audio_recording.user_id)
        )
        self._log.debug(f'End [funcName](audio_recording={audio_recording})')

        return result

    def adapt_to_output(self, audio_recording: AudioRecording) -> AudioRecordingOutput:

        self._log.debug(f'Start [funcName](audio_recording={audio_recording})')
        result: AudioRecordingOutput = AudioRecordingOutput(
            id=audio_recording.id,
            video_id=audio_recording.video_id,
            title=audio_recording.title,
            artist=audio_recording.artist,
            codec=audio_recording.codec,
            bit_rate=audio_recording.bit_rate
        )
        self._log.debug(f'End [funcName](audio_recording={audio_recording})')

        return result

    def adapt_to_output_file(self, audio_recording: AudioRecording) -> AudioOutput:

        self._log.debug(f'Start [funcName](audio_recording={audio_recording})')
        result: AudioOutput = AudioOutput(audio_recording.file_path)
        self._log.debug(f'End [funcName](audio_recording={audio_recording})')

        return result

    def adapt_to_persistence(self, audio_recording: AudioRecording, user: User) -> AudioRecordingPersistenceDomain:

        self._log.debug(f'Start [funcName](audio_recording={audio_recording}, user={user})')
        result: AudioRecordingPersistenceDomain = AudioRecordingPersistenceDomain(
            id=str(audio_recording.id),
            video_id=audio_recording.video_id,
            file_path=str(audio_recording.file_path),
            title=audio_recording.title,
            artist=audio_recording.artist,
            codec=audio_recording.codec,
            bit_rate=audio_recording.bit_rate,
            user_id=str(user.id)
        )
        self._log.debug(f'End [funcName](audio_recording={audio_recording}, user={user})')

        return result
