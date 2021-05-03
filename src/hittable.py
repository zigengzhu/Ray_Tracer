from abc import ABC, abstractmethod
from material import Material
import numpy as np
import rtxRay as ry
from aabb import AABB


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

    def bounding_box(self, time0: float, time1: float, output_box: AABB):  # return output_box
        pass


def surrounding_box(box0: AABB, box1: AABB):
    small = np.minimum(box0.minimum, box1.minimum)
    big = np.maximum(box0.maximum, box1.maximum)
    return AABB(small, big)


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

    def bounding_box(self, time0: float, time1: float, output_box: AABB):
        empty_box = AABB(np.array([0, 0, 0]), np.array([0, 0, 0]))

        if len(self.objects) == 0:
            return False, empty_box
        first_box = True
        for obj in self.objects:
            flag, box = obj.bounding_box(time0, time1, empty_box)
            if not flag:
                return False, empty_box
            if first_box:
                output_box = box
            else:
                output_box = surrounding_box(output_box, box)
            first_box = False
        return True, output_box


