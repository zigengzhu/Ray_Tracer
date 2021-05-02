import numpy as np
from rtxRay import Ray


class Camera:
    aspect_ratio: float
    viewport_height = 2.0
    viewport_width: float
    focal_length = 1.0

    origin = np.array([0.0, 0.0, 0.0])
    horizontal: np.array
    vertical: np.array
    lower_left_corner: np.array

    def __init__(self, width: int, height: int):
        self.aspect_ratio = float(width / height)
        self.viewport_width = self.aspect_ratio * self.viewport_height
        self.horizontal = np.array([self.viewport_width, 0, 0], dtype=float)
        self.vertical = np.array([0, self.viewport_height, 0], dtype=float)
        self.lower_left_corner = self.origin - self.horizontal / 2.0 - self.vertical / 2.0 - \
                                 np.array([0, 0, self.focal_length], dtype=float)

    def get_ray(self, u: float, v: float):
        return Ray(self.origin, self.lower_left_corner + u * self.horizontal + v * self.vertical - self.origin)
