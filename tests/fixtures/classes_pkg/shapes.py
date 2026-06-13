"""Fixture classes for the class-schema extractor tests (inheritance + composition)."""

import collections


class Shape:
    def __init__(self):
        self.name = "shape"

    def area(self):
        return 0


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
        self.color = Color()

    def area(self):
        return 3.14 * self.radius**2


class Color:
    def __init__(self):
        self.rgb = (0, 0, 0)


class MyList(collections.UserList):
    """Class with a dotted external base (not part of the model)."""
