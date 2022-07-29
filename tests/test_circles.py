from msspackages import *

circle = Circle(5, 'red')

def test_getters():
    assert circle.get_radius() == 5
    assert circle.get_color() == 'red'
def test_area():
    assert circle.area() == 78.53981633974483
def test_perimeter():
    assert circle.perimeter() == 31.41592653589793