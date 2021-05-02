import numpy as np


class Ray:
    origin = None
    direction = None

    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction

    def print(self):
        print("Origin: ", self.origin, " Direction", self.direction, "\n")

    def set_origin(self, x, y, z):
        self.origin = np.array([x, y, z], dtype=float)

    def set_direction(self, x, y, z):
        self.direction = np.array([x, y, z], dtype=float)

    def at(self, t):
        return self.origin + t * self.direction
