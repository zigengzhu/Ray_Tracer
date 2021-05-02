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

    u: np.array
    v: np.array
    w: np.array

    lens_radius: float

    def __init__(self, width: int, height: int,  lookfrom: np.array, lookat: np.array, vup: np.array, vfov: float,
                 aperture: float, focus_dist: float):
        self.aspect_ratio = float(width / height)
        theta = ru.deg_to_rad(vfov)
        h = np.tan(theta / 2)
        self.viewport_height = 2.0 * h
        self.viewport_width = self.aspect_ratio * self.viewport_height

        self.w = ru.unit(lookfrom - lookat)
        self.u = ru.unit(np.cross(vup, self.w))
        self.v = np.cross(self.w, self.u)

        self.origin = lookfrom
        self.horizontal = focus_dist * self.viewport_width * self.u
        self.vertical = focus_dist * self.viewport_height * self.v
        self.lower_left_corner = self.origin - self.horizontal / 2 - self.vertical / 2 - focus_dist * self.w
        self.lens_radius = aperture / 2.0

    def get_ray(self, s: float, t: float):
        rd = self.lens_radius * ru.get_random_in_unit_disk()
        offset = self.u * rd[0] + self.v * rd[1]
        return Ray(self.origin + offset, self.lower_left_corner + s * self.horizontal + t * self.vertical - self.origin
                   - offset)
