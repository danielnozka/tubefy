class InputAudioRecording:

    def __init__(self, id_: str, title: str, artist: str, codec: str, bit_rate: int):

        self.id = id_
        self.title = title
        self.artist = artist
        self.codec = codec
        self.bit_rate = bit_rate

    def __str__(self):

        return f"input_audio_recording_id='{self.id}'"
