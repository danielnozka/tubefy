from uuid import UUID


class User:

    id: UUID
    username: str
    token: str

    def __init__(self,
                 id_: UUID,
                 username: str,
                 token: str):

        self.id = id_
        self.username = username
        self.token = token

    def __str__(self) -> str:

        return f'user.id=\'{self.id}\''
