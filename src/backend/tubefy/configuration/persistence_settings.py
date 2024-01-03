import os

from pathlib import Path


class PersistenceSettings:

    data_path: Path

    def __init__(self, data_path: str):

        self.data_path = Path(os.environ.get('DATA_PATH', data_path))
