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
