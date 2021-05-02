import numpy as np
from rtxRay import Ray
import rtxUtil as ru

class Camera:
    aspect_ratio: float
    viewport_height = float
    viewport_width: float
    focal_length = 1.0

    origin = np.array
    horizontal: np.array
    vertical: np.array
    lower_left_corner: np.array

    def __init__(self, width: int, height: int,  lookfrom: np.array, lookat: np.array, vup: np.array, vfov: float):
        self.aspect_ratio = float(width / height)
        theta = ru.deg_to_rad(vfov)
        h = np.tan(theta / 2)
        self.viewport_height = 2.0 * h
        self.viewport_width = self.aspect_ratio * self.viewport_height

        w = ru.unit(lookfrom - lookat)
        u = ru.unit(np.cross(vup, w))
        v = np.cross(w, u)

        self.origin = lookfrom
        self.horizontal = self.viewport_width * u
        self.vertical = self.viewport_height * v
        self.lower_left_corner = self.origin - self.horizontal / 2 - self.vertical / 2 - w

    def get_ray(self, s: float, t: float):
        return Ray(self.origin, self.lower_left_corner + s * self.horizontal + t * self.vertical - self.origin)
