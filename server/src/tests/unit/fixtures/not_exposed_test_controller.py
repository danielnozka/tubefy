import pytest


class NotExposedTestController:

    def __init__(self):

        pass


@pytest.fixture
def not_exposed_test_controller() -> NotExposedTestController:

    return NotExposedTestController()
