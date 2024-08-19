class UsernameAlreadyRegisteredException(Exception):

    def __init__(self, username: str) -> None:

        super().__init__(f'Username \'{username}\' already registered')
