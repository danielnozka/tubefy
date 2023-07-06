import pytest


@pytest.fixture(scope='session')
def test_video_search_query() -> str:

    return 'rick astley never gonna give you up'
