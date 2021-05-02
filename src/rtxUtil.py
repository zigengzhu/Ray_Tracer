import numpy as np
from hittable import HittableList, HitRecord, Hittable
from rtxRay import Ray

pi: float = 3.1415926535897932384626433
rg = np.random.default_rng(12345)


def get_random():
    return rg.random()


def get_random_in_range(min, max):
    return min + (max - min) * get_random()


def get_random_point():
    return np.array([get_random(), get_random(), get_random()])


def get_random_point_in_range(min, max):
    return np.array([get_random_in_range(min, max), get_random_in_range(min, max), get_random_in_range(min, max)])


def get_random_in_unit_sphere():
    while True:
        point = get_random_point_in_range(-1.0, 1.0)
        if length_squared(point) >= 1:
            continue
        return point


def get_random_unit_vector():
    return unit(get_random_in_unit_sphere())


def get_random_in_hemisphere(normal: np.array):
    in_unit_sphere = get_random_in_unit_sphere()
    if in_unit_sphere.dot(normal) > 0.0:
        return in_unit_sphere
    else:
        return -in_unit_sphere


def deg_to_rad(deg):
    return deg * pi / 180.0


def length_squared(v):
    return np.sum(np.square(v))


def unit(v):
    return v / np.linalg.norm(v)


def parallel_unit(v):
    return v / np.linalg.norm(v, axis=1, keepdims=1)


def ray_color(r: Ray, world: HittableList, depth: int):
    if depth <= 0:
        return np.array([0.0, 0.0, 0.0])
    hit_anything, updated_rec = world.hit(r, 0.001, float('inf'), HitRecord())
    if hit_anything:
        target = updated_rec.p + get_random_in_hemisphere(updated_rec.normal)
        return 0.5 * ray_color(Ray(updated_rec.p, target - updated_rec.p), world, depth - 1)
    t = 0.5 * (unit(r.direction)[1] + 1.0)
    return (1.0 - t) * np.array([1.0, 1.0, 1.0]) + t * np.array([0.5, 0.7, 1.0])


def parallel_ray_color(direction):
    t = 0.5 * (parallel_unit(direction)[:, [1]] + 1.0)
    return (1.0 - t) * np.array([1.0, 1.0, 1.0]) + t * np.array([0.5, 0.7, 1.0])


def color_to_str(color, samples_per_pixel):
    color = np.sqrt(color * (1.0 / samples_per_pixel))
    color[0] = 256.0 * clamp(color[0], 0.0, 0.999)
    color[1] = 256.0 * clamp(color[1], 0.0, 0.999)
    color[2] = 256.0 * clamp(color[2], 0.0, 0.999)
    return str(int(color[0])) + ' ' + str(int(color[1])) + ' ' + str(int(color[2])) + '\n'


def clamp(x: float, min: float, max: float):
    if x < min:
        return min
    if x > max:
        return max
    return x
