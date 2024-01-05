import os


class SecuritySettings:

    json_web_token_algorithm: str
    json_web_token_expiration_minutes: float
    json_web_token_key: str

    def __init__(
        self,
        json_web_token_algorithm: str,
        json_web_token_expiration_minutes: float,
        json_web_token_key: str
    ):

        self.json_web_token_algorithm = os.environ.get('JSON_WEB_TOKEN_ALGORITHM', json_web_token_algorithm)
        self.json_web_token_expiration_minutes = float(
            os.environ.get('JSON_WEB_TOKEN_EXPIRATION_MINUTES', json_web_token_expiration_minutes)
        )
        self.json_web_token_key = os.environ.get('JSON_WEB_TOKEN_KEY', json_web_token_key)
