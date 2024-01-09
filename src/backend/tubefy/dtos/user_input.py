from fastapi.security import OAuth2PasswordRequestForm


class UserInput(OAuth2PasswordRequestForm):

    def __str__(self) -> str:

        return f'{self.__class__.__name__}(username=\'{self.username}\')'
