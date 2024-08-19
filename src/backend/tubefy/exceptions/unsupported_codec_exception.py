class UnsupportedCodecException(Exception):

    def __init__(self, codec: str) -> None:

        super().__init__(f'Codec \'{codec}\' is not a supported value)')
