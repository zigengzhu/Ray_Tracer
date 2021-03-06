import numpy as np
from hittable import HittableList, HitRecord
from rtxRay import Ray

rg = np.random.default_rng(12345)


def refract(uv: np.array, n: np.array, etai_over_etat: float):
    cos_theta = np.minimum(-uv.dot(n), 1.0)
    r_out_perp = etai_over_etat * (uv + cos_theta * n)
    r_out_parallel = -np.sqrt(np.abs(1.0 - length_squared(r_out_perp))) * n
    return r_out_perp + r_out_parallel


def near_zero(v: np.array):
    s = 1e-8
    return np.abs(v[0]) < s and np.abs(v[1]) < s and np.abs(v[2]) < s


def reflect(v: np.array, n: np.array):
    return v - 2.0 * v.dot(n) * n


def get_random():
    return rg.random()


def get_random_int_in_range(min, max):
    return int(get_random_in_range(min, max + 1))


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


def get_random_in_unit_disk():
    while True:
        p = np.array([get_random_in_range(-1, 1), get_random_in_range(-1, 1), 0])
        if length_squared(p) >= 1.0:
            continue
        return p


def deg_to_rad(deg):
    return deg * np.pi / 180.0


def length_squared(v):
    return np.sum(np.square(v))


def length(v):
    return np.sqrt(np.sum(np.square(v)))


def unit(v):
    return v / np.linalg.norm(v)


def parallel_unit(v):
    return v / np.linalg.norm(v, axis=1, keepdims=1)


def ray_color(r: Ray, background: np.array, world: HittableList, depth: int):
    if depth <= 0:
        return np.array([0.0, 0.0, 0.0])

    hit_anything, updated_rec = world.hit(r, 0.001, float('inf'), HitRecord())
    if not hit_anything:
        return background
    emitted = updated_rec.mat.emitted(updated_rec.u, updated_rec.v, updated_rec.p)

    is_scatter, scattered, attenuation = updated_rec.mat.scatter(r, updated_rec)
    if not is_scatter:
        return emitted

    return emitted + attenuation * ray_color(scattered, background, world, depth - 1)

        #return np.array([0.0, 0.0, 0.0])
        # target = updated_rec.p + get_random_in_hemisphere(updated_rec.normal)
        # return 0.5 * ray_color(Ray(updated_rec.p, target - updated_rec.p), world, depth - 1)
    #t = 0.5 * (unit(r.direction)[1] + 1.0)
    #return (1.0 - t) * np.array([1.0, 1.0, 1.0]) + t * np.array([0.5, 0.7, 1.0])


def parallel_ray_color(direction):
    t = 0.5 * (parallel_unit(direction)[:, [1]] + 1.0)
    return (1.0 - t) * np.array([1.0, 1.0, 1.0]) + t * np.array([0.5, 0.7, 1.0])


def color_to_str(color, samples_per_pixel):
    color = np.sqrt(color * (1.0 / samples_per_pixel))
    color[0] = 256.0 * clamp(color[0], 0.0, 0.999)
    color[1] = 256.0 * clamp(color[1], 0.0, 0.999)
    color[2] = 256.0 * clamp(color[2], 0.0, 0.999)
    return str(int(color[0])) + ' ' + str(int(color[1])) + ' ' + str(int(color[2])) + '\n'


def clamp(x: float, minimum: float, maximum: float):
    if x < minimum:
        return minimum
    if x > maximum:
        return maximum
    return x
