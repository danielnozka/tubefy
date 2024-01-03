import logging

from dependency_injector.wiring import inject, Provide
from logging import Logger

from ..configuration import AppSettings
from .domain import DatabaseUser
from .database_context import DatabaseContext
from ..services import DirectoryHandler


class UsersPersistence:

    _log: Logger = logging.getLogger(__name__)
    _database_context: DatabaseContext

    @inject
    def __init__(
        self,
        app_settings: AppSettings = Provide['app_settings'],
        directory_handler: DirectoryHandler = Provide['directory_handler']
    ):

        self._database_context = DatabaseContext(
            directory_handler.create_directory(app_settings.persistence_settings.data_path)
        )

    def close(self) -> None:

        self._database_context.close()

    def get_user(self, username: str) -> DatabaseUser | None:

        self._log.debug(f'Start [funcName](username=\'{username}\')')
        result = self._database_context.get_user(username)
        self._log.debug(f'End [funcName](username=\'{username}\')')

        return result

    def add_user(self, database_user: DatabaseUser) -> None:

        self._log.debug(f'Start [funcName](database_user={database_user})')
        self._database_context.add_user(database_user)
        self._log.debug(f'End [funcName](database_user={database_user})')
