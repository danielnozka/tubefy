from fastapi.security import OAuth2PasswordRequestForm


class UserCredentialsDto(OAuth2PasswordRequestForm):

    def __repr__(self) -> str:

        return f'{self.__class__.__name__}(username=\'{self.username}\')'
