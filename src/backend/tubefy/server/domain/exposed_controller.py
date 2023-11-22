from .exposed_method import ExposedMethod


class ExposedController:

    name: str
    route: str | None
    exposed_methods: list[ExposedMethod]

    def __init__(self,
                 name: str,
                 route: str | None):

        self.name = name
        self.route = route
        self.exposed_methods = []
