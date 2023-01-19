from devex_sdk import add


def test_add():
    assert add(1,2) == 3
    assert add(5,7) == 12
    assert add(1,1) == 2
    assert add(-2,1) == -1