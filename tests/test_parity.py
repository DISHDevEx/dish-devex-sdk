import msspackages as mss

num_odd = mss.Number(5)
num_even = mss.Number(2)

def test_odd():
    assert num_odd.parity() == 'odd'

def test_even():
    assert num_even.parity() == 'even'