class AppBaseException(Exception):

    status_code: int
    headers: dict[str, str] | None

    def __init__(self, status_code: int, message: str, headers: dict[str, str] | None = None) -> None:

        self.status_code = status_code
        self.headers = headers
        super().__init__(message)
