import pytest


@pytest.fixture(scope='session')
def test_search_query() -> str:

    return 'rick astley never gonna give you up'
