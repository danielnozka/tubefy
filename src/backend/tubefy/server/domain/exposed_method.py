from .http_method import HttpMethod


class ExposedMethod:

    name: str
    route: str
    http_method: HttpMethod

    def __init__(self,
                 name: str,
                 route: str,
                 http_method: HttpMethod):

        self.name = name
        self.route = route
        self.http_method = http_method
