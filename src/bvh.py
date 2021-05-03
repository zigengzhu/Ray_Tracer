from hittable import Hittable, HitRecord, surrounding_box
import rtxRay as ry
import rtxUtil as ru
from abc import ABC
from aabb import AABB
import numpy as np

empty = np.array([0.0, 0.0, 0.0])


def box_compare(a: Hittable, b: Hittable, axis: int):
    box_a = AABB(empty, empty)
    box_b = AABB(empty, empty)
    flag_a, box_a = a.bounding_box(0, 0, box_a)
    flag_b, box_b = b.bounding_box(0, 0, box_b)
    if not flag_a or not flag_b:
        print("No bounding box in bvh_node constructor")
        raise
    return box_a.minimum[axis] < box_b.minimum[axis]


"""
def box_x_compare(a: Hittable, b: Hittable):
    return box_compare(a, b, 0)

def box_y_compare(a: Hittable, b: Hittable):
    return box_compare(a, b, 1)

def box_z_compare(a: Hittable, b: Hittable):
    return box_compare(a, b, 2)
"""


class BVHNode(Hittable, ABC):
    left: Hittable
    right: Hittable
    box: AABB

    """
        def __init__(self, list: HittableList, time0: float, time1: float):
            self.recursive_init(list.objects, 0, len(list.objects), time0, time1)
    """

    def __init__(self, src_objects, start: int, end: int, time0: float, time1: float):
        objects = src_objects
        axis = ru.get_random_int_in_range(0, 2)
        object_span = end - start
        if object_span == 1:
            self.left = objects[start]
            self.right = objects[start]
        elif object_span == 2:
            if box_compare(objects[start], objects[start + 1], axis):
                self.left = objects[start]
                self.right = objects[start + 1]
            else:
                self.left = objects[start+1]
                self.right = objects[start]
        else:
            objects[start:end] = sorted(objects[start:end], key=lambda x: x.min_box[axis])
            mid = int(start + object_span / 2)
            self.left = BVHNode(objects, start, mid, time0, time1)
            self.right = BVHNode(objects, mid, end, time0, time1)

        box_left = AABB(empty, empty)
        box_right = AABB(empty, empty)
        flag_left, box_left = self.left.bounding_box(time0, time1, box_left)
        flag_right, box_right = self.right.bounding_box(time0, time1, box_right)

        if not flag_left or not flag_right:
            print("No bounding box in bvh_node constructor.")
            raise
        self.box = surrounding_box(box_left, box_right)

    def bounding_box(self, time0: float, time1: float, output_box: AABB):
        return True, self.box

    def hit(self, r: ry.Ray, t_min: float, t_max: float, rec: HitRecord):
        if not self.box.hit(r, t_min, t_max):
            return False
        hit_left = self.left.hit(r, t_min, t_max, rec)
        if hit_left:
            t_max = rec.t
        hit_right = self.right.hit(r, t_min, t_max, rec)
        return hit_left or hit_right