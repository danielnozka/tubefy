class UsernameAlreadyRegisteredException(Exception):

    status_code: int = 409

    def __init__(self, username: str):

        super().__init__(f'Username \'{username}\' already registered')
