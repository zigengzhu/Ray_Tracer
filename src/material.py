from abc import ABC, abstractmethod

from rtxRay import Ray
import rtxUtil as ru
import numpy as np


class Material(ABC):
    @abstractmethod
    def scatter(self, r_in: Ray, rec):
        pass


class Lambertian(Material, ABC):
    albedo: np.array

    def __init__(self, albedo: np.array):
        self.albedo = albedo

    def scatter(self, r_in: Ray, rec):
        scatter_direction = rec.normal + ru.get_random_unit_vector()
        if ru.near_zero(scatter_direction):
            scatter_direction = rec.normal
        scattered = Ray(rec.p, scatter_direction)
        attenuation = self.albedo
        return True, scattered, attenuation


class Metal(Material, ABC):
    albedo: np.array
    fuzz: float

    def __init__(self, albedo: np.array, fuzz: float):
        self.albedo = albedo
        if fuzz < 1.0:
            self.fuzz = fuzz
        else:
            self.fuzz = 1.0

    def scatter(self, r_in: Ray, rec):
        reflected = ru.reflect(ru.unit(r_in.direction), rec.normal)
        scattered = Ray(rec.p, reflected + self.fuzz * ru.get_random_in_unit_sphere())
        attenuation = self.albedo
        return scattered.direction.dot(rec.normal) > 0, scattered, attenuation


class Dielectric(Material, ABC):
    ir: float

    def __init__(self, ir: float):
        self.ir = ir

    def scatter(self, r_in: Ray, rec):
        attenuation = np.array([1.0, 1.0, 1.0])
        refraction_ratio: float
        if rec.front_face:
            refraction_ratio = 1.0 / self.ir
        else:
            refraction_ratio = self.ir
        unit_direction = ru.unit(r_in.direction)
        cos_theta = np.min(-unit_direction.dot(rec.normal), 1.0)
        sin_theta = np.sqrt(1.0 - cos_theta * cos_theta)
        cannot_refract = refraction_ratio * sin_theta > 1.0
        direction: np.array
        if cannot_refract or self.reflectance(cos_theta, refraction_ratio) > ru.get_random():
            direction = ru.reflect(unit_direction, rec.normal)
        else:
            direction = ru.refract(unit_direction, rec.normal, refraction_ratio)
        scattered = Ray(rec.p, direction)
        return True, scattered, attenuation

    def reflectance(self, cosine: float, ri: float):
        r0 = (1 - ri) / (1 + ri)
        r0 *= r0
        return r0 + (1 - r0) * np.power((1 - cosine), 5)
