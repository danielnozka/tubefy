from dataclasses import dataclass, field


@dataclass
class UserCredentials:

    username: str
    password: str = field(repr=False)
