import logging
from dependency_injector.wiring import inject, Provide
from logging import Logger
from uuid import UUID
from ..adapters.audio_recording_adapter import AudioRecordingAdapter
from ..domain.audio_recording import AudioRecording
from ..domain.user import User
from ..dtos.audio_output import AudioOutput
from ..dtos.audio_recording_output import AudioRecordingOutput
from ..exceptions.audio_file_not_found_exception import AudioFileNotFoundException
from ..exceptions.audio_recording_not_found_exception import AudioRecordingNotFoundException


class AudioRecordingGetter:

    _log: Logger = logging.getLogger(__name__)
    _audio_recording_adapter: AudioRecordingAdapter

    @inject
    def __init__(self, audio_recording_adapter: AudioRecordingAdapter = Provide['audio_recording_adapter']) -> None:

        self._audio_recording_adapter = audio_recording_adapter

    def get_all(self, user: User) -> list[AudioRecordingOutput]:

        self._log.debug(f'Start [funcName](user={user})')
        result: list[AudioRecordingOutput] = [
            self._audio_recording_adapter.adapt_to_output(x) for x in user.audio_recordings
        ]
        self._log.debug(f'End [funcName](user={user})')

        return result

    def get(self, audio_recording_id: UUID, user: User) -> AudioOutput:

        self._log.debug(f'Start [funcName](audio_recording_id=\'{audio_recording_id}\', user={user})')
        audio_recording: AudioRecording | None = next(
            (x for x in user.audio_recordings if x.id == audio_recording_id),
            None
        )

        if audio_recording is None:

            raise AudioRecordingNotFoundException(audio_recording_id)

        else:

            if audio_recording.file_path.is_file():

                result: AudioOutput = self._audio_recording_adapter.adapt_to_output_file(audio_recording)
                self._log.debug(f'End [funcName](audio_recording_id=\'{audio_recording_id}\', user={user})')

                return result

            else:

                raise AudioFileNotFoundException(audio_recording.file_path)
