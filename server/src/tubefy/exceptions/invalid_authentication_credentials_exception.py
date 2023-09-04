class InvalidAuthenticationCredentialsException(Exception):

    status_code: int = 401

    def __init__(self):

        super().__init__('Invalid username or password')
