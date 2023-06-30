class InputAudioRecordingOptions:

    title: str
    artist: str
    codec: str
    bit_rate: int

    def __init__(self,
                 title: str,
                 artist: str,
                 codec: str,
                 bit_rate: int):

        self.title = title
        self.artist = artist
        self.codec = codec
        self.bit_rate = bit_rate

    def __str__(self) -> str:

        return (f'input_audio_recording_options.title=\'{self.title}\', '
                f'input_audio_recording_options.artist=\'{self.artist}\', '
                f'input_audio_recording_options.codec=\'{self.codec}\', '
                f'input_audio_recording_options.bit_rate={self.bit_rate}')
