import pytest

from .fixtures.exposed_test_controller import ExposedTestController
from .fixtures.non_exposed_test_controller import NonExposedTestController
from youtube_music_manager_server.exceptions.controller_not_exposed_exception import ControllerNotExposedException
from youtube_music_manager_server.server import Server


class ServerTest:

    @staticmethod
    def test_exposed_controller_is_registered(server: Server, exposed_test_controller: ExposedTestController) -> None:

        server.register_controller(exposed_test_controller)

    @staticmethod
    def test_non_exposed_controller_raises_exception(server: Server,
                                                     non_exposed_test_controller: NonExposedTestController) -> None:

        with pytest.raises(ControllerNotExposedException):

            server.register_controller(non_exposed_test_controller)

    @staticmethod
    def test_server_starts(server: Server,) -> None:

        server.start(testing=True)

    @staticmethod
    def test_server_stops(server: Server,) -> None:

        server.stop()
