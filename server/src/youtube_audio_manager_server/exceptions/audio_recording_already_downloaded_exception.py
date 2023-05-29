class AudioRecordingAlreadyDownloadedException(Exception):

    status_code = 409

    def __init__(self, audio_id: str):

        super().__init__(f'Audio recording with ID \'{audio_id}\' already downloaded')
