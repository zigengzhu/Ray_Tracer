from abc import ABC
import numpy as np
import rtxRay as ry
from hittable import Hittable, HitRecord
from aabb import AABB

empty = np.array([0.0, 0.0, 0.0])

class XYRectangle(Hittable, ABC):
    material = None
    min_box = None
    x0: float
    x1: float
    y0: float
    y1: float
    k: float

    def __init__(self, x0, x1, y0, y1, k, mat):
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1
        self.k = k
        self.material = mat
        box = AABB(empty, empty)
        flag, box = self.bounding_box(0, 0, box)
        if not flag:
            print("No sort key")
            raise
        self.min_box = box.minimum

    def bounding_box(self, time0: float, time1: float, output_box: AABB):
        output_box = AABB(np.array([self.x0, self.y0, self.k - 0.0001]), np.array([self.x1, self.y1, self.k + 0.0001]))
        return True, output_box

    def hit(self, r: ry.Ray, t_min: float, t_max: float, rec: HitRecord):
        t = (self.k - r.origin[2]) / r.direction[2]
        if t < t_min or t > t_max:
            return False
        x = r.origin[0] + t * r.direction[0]
        y = r.origin[1] + t * r.direction[1]

        if x < self.x0 or x > self.x1 or y < self.y0 or y > self.y1:
            return False

        rec.u = (x - self.x0) / (self.x1 - self.x0)
        rec.v = (y - self.y0) / (self.y1 - self.y0)
        rec.t = t
        outward_normal = np.array([0, 0, 1])
        rec.set_face_normal(r, outward_normal)
        rec.mat = self.material
        rec.p = r.at(t)
        return True, rec


class XZRectangle(Hittable, ABC):
    material = None
    min_box = None
    x0: float
    x1: float
    z0: float
    z1: float
    k: float

    def __init__(self, x0, x1, z0, z1, k, mat):
        self.x0 = x0
        self.x1 = x1
        self.z0 = z0
        self.z1 = z1
        self.k = k
        self.material = mat
        box = AABB(empty, empty)
        flag, box = self.bounding_box(0, 0, box)
        if not flag:
            print("No sort key")
            raise
        self.min_box = box.minimum

    def bounding_box(self, time0: float, time1: float, output_box: AABB):
        output_box = AABB(np.array([self.x0, self.k - 0.0001, self.z0]), np.array([self.x1, self.k + 0.0001, self.z1]))
        return True, output_box

    def hit(self, r: ry.Ray, t_min: float, t_max: float, rec: HitRecord):
        t = (self.k - r.origin[1]) / r.direction[1]
        if t < t_min or t > t_max:
            return False
        x = r.origin[0] + t * r.direction[0]
        z = r.origin[2] + t * r.direction[2]

        if x < self.x0 or x > self.x1 or z < self.z0 or z > self.z1:
            return False

        rec.u = (x - self.x0) / (self.x1 - self.x0)
        rec.v = (z - self.z0) / (self.z1 - self.z0)
        rec.t = t
        outward_normal = np.array([0, 1, 0])
        rec.set_face_normal(r, outward_normal)
        rec.mat = self.material
        rec.p = r.at(t)
        return True, rec


class YZRectangle(Hittable, ABC):
    material = None
    min_box = None
    y0: float
    y1: float
    z0: float
    z1: float
    k: float

    def __init__(self, y0, y1, z0, z1, k, mat):
        self.y0 = y0
        self.y1 = y1
        self.z0 = z0
        self.z1 = z1
        self.k = k
        self.material = mat
        box = AABB(empty, empty)
        flag, box = self.bounding_box(0, 0, box)
        if not flag:
            print("No sort key")
            raise
        self.min_box = box.minimum

    def bounding_box(self, time0: float, time1: float, output_box: AABB):
        output_box = AABB(np.array([self.k - 0.0001, self.y0, self.z0]), np.array([self.k + 0.0001, self.y1, self.z1]))
        return True, output_box

    def hit(self, r: ry.Ray, t_min: float, t_max: float, rec: HitRecord):
        t = (self.k - r.origin[0]) / r.direction[0]
        if t < t_min or t > t_max:
            return False
        y = r.origin[1] + t * r.direction[1]
        z = r.origin[2] + t * r.direction[2]

        if y < self.y0 or y > self.y1 or z < self.z0 or z > self.z1:
            return False

        rec.u = (y - self.y0) / (self.y1 - self.y0)
        rec.v = (z - self.z0) / (self.z1 - self.z0)
        rec.t = t
        outward_normal = np.array([1, 0, 0])
        rec.set_face_normal(r, outward_normal)
        rec.mat = self.material
        rec.p = r.at(t)
        return True, rec