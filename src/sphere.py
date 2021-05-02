from abc import ABC
import numpy as np
import rtxRay as ry
import rtxUtil as ru
from hittable import Hittable, HitRecord


class Sphere(Hittable, ABC):
    center = None
    radius = None
    material = None

    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def hit(self, r: ry.Ray, t_min: float, t_max: float, rec: HitRecord):
        oc = r.origin - self.center
        a = ru.length_squared(r.direction)
        half_b = oc.dot(r.direction)
        c = ru.length_squared(oc) - self.radius * self.radius

        discriminant = half_b * half_b - a * c
        if discriminant < 0:
            return False

        sqrt_discriminant = np.sqrt(discriminant)

        root = (-half_b - sqrt_discriminant) / a
        if root < t_min or t_max < root:
            root = (-half_b + sqrt_discriminant) / a
            if root < t_min or t_max < root:
                return False

        rec.t = root
        rec.p = r.at(rec.t)
        outward_normal = (rec.p - self.center) / self.radius
        rec.set_face_normal(r, outward_normal)
        rec.mat = self.material
        return True
