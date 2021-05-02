from abc import ABC, abstractmethod
from material import Material
import numpy as np
import rtxRay as ry


class HitRecord:
    p: np.array
    normal: np.array
    mat: Material
    t: float
    front_face: bool

    def __init__(self):
        self.p = None
        self.normal = None
        self.t = 0
        self.front_face = False

    def set_face_normal(self, r: ry.Ray, outward_normal: np.array):
        self.front_face = r.direction.dot(outward_normal) < 0
        if self.front_face:
            self.normal = outward_normal
        else:
            self.normal = -outward_normal


class Hittable(ABC):
    @abstractmethod
    def hit(self, r: ry.Ray, t_min: float, t_max: float, rec: HitRecord):
        pass


class HittableList(Hittable, ABC):
    objects = None

    def __init__(self):
        self.objects = []

    def add(self, obj):
        self.objects.append(obj)

    def clear(self):
        self.objects.clear()

    def hit(self, r: ry.Ray, t_min: float, t_max: float, rec: HitRecord):
        temp_rec = HitRecord()
        hit_anything = False
        closest_so_far = t_max

        for obj in self.objects:
            if obj.hit(r, t_min, closest_so_far, temp_rec):
                hit_anything = True
                closest_so_far = temp_rec.t
        return hit_anything, temp_rec








