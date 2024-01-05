import os

from pathlib import Path


class PersistenceSettings:

    data_path: Path
    audio_samples_deletion_interval_hours: float

    def __init__(self, data_path: str, audio_samples_deletion_interval_hours: float):

        self.data_path = Path(os.environ.get('DATA_PATH', data_path))
        self.audio_samples_deletion_interval_hours = float(
            os.environ.get('AUDIO_SAMPLES_DELETION_INTERVAL_HOURS', audio_samples_deletion_interval_hours)
        )
