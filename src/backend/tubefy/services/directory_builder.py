from pathlib import Path


class DirectoryBuilder:

    _root_path: Path

    def __init__(self, root_path: Path):

        self._root_path = root_path

    def build(self, directory_path: Path) -> Path:

        directory_absolute_path = self._get_directory_absolute_path(directory_path)
        directory_absolute_path.mkdir(parents=True, exist_ok=True)

        return directory_absolute_path

    def _get_directory_absolute_path(self, directory_path: Path) -> Path:

        if directory_path.is_absolute():

            return directory_path.resolve()

        else:

            return self._root_path.joinpath(directory_path).resolve()
