import pytest

from youtube_music_manager_server.main import Main


@pytest.fixture(scope='package', autouse=True)
def run_main() -> None:

    main = Main()
    main.start(testing=True)
