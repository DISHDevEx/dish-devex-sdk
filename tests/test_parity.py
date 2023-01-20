import devex_sdk

num_odd = devex_sdk.Number(5)
num_even = devex_sdk.Number(2)

def test_odd():
    assert num_odd.parity() == 'odd'

def test_even():
    assert num_even.parity() == 'even'