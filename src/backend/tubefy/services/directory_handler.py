import logging

from aiopath import AsyncPath
from logging import Logger
from pathlib import Path


class DirectoryHandler:

    _log: Logger = logging.getLogger(__name__)
    _root_path: Path

    def __init__(self, root_path: Path) -> None:

        self._root_path = root_path

    def create_directory(self, directory_path: Path) -> Path:

        directory_absolute_path: Path = self._get_directory_absolute_path(directory_path)

        if not directory_absolute_path.exists() and not directory_absolute_path.is_dir():

            self._log.debug(f'Start [funcName](directory_path=\'{directory_absolute_path}\')')
            directory_absolute_path.mkdir(parents=True, exist_ok=True)
            self._log.debug(f'End [funcName](directory_path=\'{directory_absolute_path}\')')

        return directory_absolute_path

    async def create_directory_async(self, directory_path: Path) -> Path:

        directory_absolute_path: Path = self._get_directory_absolute_path(directory_path)

        if not directory_absolute_path.exists() and not directory_absolute_path.is_dir():

            self._log.debug(f'Start [funcName](directory_path=\'{directory_absolute_path}\')')
            await AsyncPath(directory_absolute_path).mkdir(parents=True, exist_ok=True)
            self._log.debug(f'End [funcName](directory_path=\'{directory_absolute_path}\')')

        return directory_absolute_path

    def delete_directory(self, directory_path: Path) -> None:

        directory_absolute_path: Path = self._get_directory_absolute_path(directory_path)

        self._log.debug(f'Start [funcName](directory_path=\'{directory_absolute_path}\')')

        if directory_absolute_path.exists() and directory_absolute_path.is_dir():

            self._delete_directory_recursively(directory_absolute_path)

        else:

            self._log.warning(f'Path \'{directory_absolute_path}\' does not exist or it is not a directory')

        self._log.debug(f'End [funcName](directory_path=\'{directory_absolute_path}\')')

    def _get_directory_absolute_path(self, directory_path: Path) -> Path:

        if directory_path.is_absolute():

            return directory_path.resolve()

        else:

            return self._root_path.joinpath(directory_path).resolve()

    def _delete_directory_recursively(self, directory_path: Path) -> None:

        item: Path
        for item in directory_path.iterdir():

            if item.is_file():

                try:

                    item.unlink()

                except Exception as exception:

                    self._log.warning(
                        msg=f'Exception found while deleting file \'{item}\'',
                        extra={'exception': exception}
                    )

            elif item.is_dir():

                self._delete_directory_recursively(item)

        try:

            directory_path.rmdir()

        except Exception as exception:

            self._log.warning(
                msg=f'Exception found while deleting directory \'{directory_path}\'',
                extra={'exception': exception}
            )
