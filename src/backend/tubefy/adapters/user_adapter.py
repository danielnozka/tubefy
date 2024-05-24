import logging
from dependency_injector.wiring import inject, Provide
from logging import Logger
from uuid import UUID, uuid4
from ..adapters.audio_recording_adapter import AudioRecordingAdapter
from ..domain.user import User
from ..dtos.user_input import UserInput
from ..persistence.domain.user_persistence_domain import UserPersistenceDomain
from ..services.password_hash_handler import PasswordHashHandler


class UserAdapter:

    _log: Logger = logging.getLogger(__name__)
    _audio_recording_adapter: AudioRecordingAdapter
    _password_hash_handler: PasswordHashHandler

    @inject
    def __init__(
        self,
        audio_recording_adapter: AudioRecordingAdapter = Provide['audio_recording_adapter'],
        password_hash_handler: PasswordHashHandler = Provide['password_hash_handler']
    ) -> None:

        self._audio_recording_adapter = audio_recording_adapter
        self._password_hash_handler = password_hash_handler

    def adapt_from_persistence(self, user: UserPersistenceDomain) -> User:

        self._log.debug(f'Start [funcName](user={user})')
        result: User = User(
            id=UUID(user.id),
            username=user.username,
            audio_recordings=[
                self._audio_recording_adapter.adapt_from_persistence(x)
                for x in user.audio_recordings
            ]
        )
        self._log.debug(f'End [funcName](user={user})')

        return result

    def adapt_to_persistence(self, user: UserInput) -> UserPersistenceDomain:

        self._log.debug(f'Start [funcName](user={user})')
        result: UserPersistenceDomain = UserPersistenceDomain(
            id=str(uuid4()),
            username=user.username,
            password=self._password_hash_handler.hash_password(user.password)
        )
        self._log.debug(f'End [funcName](user={user})')

        return result
