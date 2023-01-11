"""
Demonstrate a class with attributes and methods
and an additional function that acts on objects from that class.
"""


import math

class Circle:
    """Example class with attributes and methods"""
    def __init__(self, radius, color):
        self.radius = radius
        self.color = color

    def get_radius(self):
        """Get radius of the circle."""
        return self.radius

    def get_color(self):
        """Get color of the circle."""
        return self.color

    def area(self):
        """Get area of the circle."""
        return math.pi*(self.radius*self.radius)

    def perimeter(self):
        """Get perimeter of the circle."""
        return 2*math.pi*self.radius

def describe(circle):
    """Example function acting on an object"""
    print(f"This is a {circle.color} circle with a radius of {circle.radius}.")
    