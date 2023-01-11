"""
Demonstrate a class with attributes and methods
and an additional function that acts on objects from that class.
"""


import math

class Circle:
    def __init__(self, radius, color):
        self.radius = radius
        self.color = color

    def get_radius(self):
        return self.radius

    def get_color(self):
        return self.color

    def area(self):
        return math.pi*(self.radius*self.radius)

    def perimeter(self):
        return 2*math.pi*self.radius

def describe(circle):
    print(f"This is a {circle.color} circle with a radius of {circle.radius}.")
    