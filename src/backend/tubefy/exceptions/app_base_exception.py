class AppBaseException(Exception):

    status_code: int
    detail: str
    headers: dict[str, str] | None

    def __init__(self, status_code: int, detail: str, headers: dict[str, str] | None = None):

        self.status_code = status_code
        self.detail = detail
        self.headers = headers
        super().__init__(detail)
