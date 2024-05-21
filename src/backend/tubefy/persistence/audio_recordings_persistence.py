import logging

from dependency_injector.wiring import inject, Provide
from logging import Logger
from pathlib import Path
from uuid import UUID

from ..domain.user import User
from ..dtos.audio_download_options_input import AudioDownloadOptionsInput
from .app_persistence_context import AppPersistenceContext
from .domain.audio_recording_persistence_domain import AudioRecordingPersistenceDomain


class AudioRecordingsPersistence:

    _log: Logger = logging.getLogger(__name__)
    _context: AppPersistenceContext

    @inject
    def __init__(self, context: AppPersistenceContext = Provide['app_persistence_context']) -> None:

        self._context = context

    async def get_audio_recording(self, audio_recording_id: UUID) -> AudioRecordingPersistenceDomain | None:

        self._log.debug(f'Start [funcName](audio_recording_id=\'{audio_recording_id}\')')
        result: AudioRecordingPersistenceDomain | None = await self._context.get_audio_recording(audio_recording_id)
        self._log.debug(f'End [funcName](audio_recording_id=\'{audio_recording_id}\')')

        return result

    async def add_audio_recording(self, audio_recording: AudioRecordingPersistenceDomain) -> None:

        self._log.debug(f'Start [funcName](audio_recording={audio_recording})')
        await self._context.add_audio_recording(audio_recording)
        self._log.debug(f'End [funcName](audio_recording={audio_recording})')

    async def delete_audio_recording(self, audio_recording: AudioRecordingPersistenceDomain) -> None:

        self._log.debug(f'Start [funcName](audio_recording={audio_recording})')
        await self._context.delete_audio_recording(audio_recording)
        self._log.debug(f'End [funcName](audio_recording={audio_recording})')

    async def get_user_audio_recordings_directory(self, user: User) -> Path:

        return await self._context.get_user_audio_recordings_directory(user.id)

    def get_audio_recording_filename(self, audio_download_options_input: AudioDownloadOptionsInput) -> str:

        return self._context.get_audio_recording_filename(
            artist=audio_download_options_input.artist,
            title=audio_download_options_input.title
        )
