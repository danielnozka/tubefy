class AuthenticationSettings:

    json_web_token_secret_key: str

    def __init__(self, json_web_token_secret_key: str):

        self.json_web_token_secret_key: str = json_web_token_secret_key
