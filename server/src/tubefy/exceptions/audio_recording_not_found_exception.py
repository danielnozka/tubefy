from uuid import UUID


class AudioRecordingNotFoundException(Exception):

    status_code: int = 404

    def __init__(self, recording_id: UUID):

        super().__init__(f'Audio recording with ID \'{recording_id}\' does not exist')
