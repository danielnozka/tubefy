class AudioRecordingNotFoundException(Exception):

    status_code = 404

    def __init__(self, audio_id: str):

        super().__init__(f'Audio recording with ID \'{audio_id}\' does not exist')
