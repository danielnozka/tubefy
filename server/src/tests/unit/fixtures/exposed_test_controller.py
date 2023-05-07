import pytest

from youtube_music_manager_server.tools.server import route


@route('/test')
class ExposedTestController:

    def __init__(self):

        pass


@pytest.fixture
def exposed_test_controller() -> ExposedTestController:

    return ExposedTestController()
