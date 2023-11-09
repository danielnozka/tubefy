from uuid import UUID


class OutputAuthentication:

    user_id: UUID
    token: str

    def __init__(self,
                 user_id: UUID,
                 token: str):

        self.user_id = user_id
        self.token = token
