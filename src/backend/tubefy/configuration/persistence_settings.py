import os

from dependency_injector.wiring import inject, Provide
from pathlib import Path

from ..services import DirectoryBuilder


class PersistenceSettings:

    audio_database_directory_path: Path
    audio_files_directory_path: Path

    @inject
    def __init__(
        self,
        audio_database_directory_path: str,
        audio_files_directory_path: str,
        directory_builder: DirectoryBuilder = Provide['directory_builder']
    ):

        self.audio_database_directory_path = directory_builder.build(
            Path(os.environ.get('AUDIO_DATABASE_DIRECTORY_PATH', audio_database_directory_path))
        )
        self.audio_files_directory_path = directory_builder.build(
            Path(os.environ.get('AUDIO_FILES_DIRECTORY_PATH', audio_files_directory_path))
        )
