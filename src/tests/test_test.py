import pytest

@pytest.fixture
def input_value():
    return 100

def test_parser(input_value):
    assert input_value == 100