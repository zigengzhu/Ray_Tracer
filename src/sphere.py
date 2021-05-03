from abc import ABC
import numpy as np
import rtxRay as ry
import rtxUtil as ru
from hittable import Hittable, HitRecord
from aabb import AABB

empty = np.array([0.0, 0.0, 0.0])


class Sphere(Hittable, ABC):
    center = None
    radius = None
    material = None
    min_box = None

    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

        box = AABB(empty, empty)
        flag, box = self.bounding_box(0, 0, box)
        if not flag:
            print("No sort key")
            raise
        self.min_box = box.minimum


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

    def bounding_box(self, time0: float, time1: float, output_box: AABB):
        output_box = AABB(
            self.center - np.array([self.radius, self.radius, self.radius]),
            self.center + np.array([self.radius, self.radius, self.radius])
        )
        return True, output_box
