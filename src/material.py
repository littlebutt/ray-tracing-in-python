from typing import Tuple
from hittable import HitRecord
from ray import Ray
from utils import near_zero, random_unit_vector
from vec import Color, Vector3


__all__ = ['Material', 'Lambertian', 'Metal']


class Material:

    def scatter(self, r_in: "Ray", rec: "HitRecord") -> Tuple[bool, "Color", "Ray"]:
        return False


class Lambertian(Material):

    def __init__(self, albedo: "Color") -> None:
        self.albedo = albedo

    def scatter(self, r_in: Ray, rec: HitRecord) -> Tuple[bool | Color | Ray]:
        scatter_direction = rec.normal + random_unit_vector()
        if near_zero(scatter_direction):
            scatter_direction = rec.normal
        return True, self.albedo, Ray(rec.p, scatter_direction)


class Metal(Material):

    def __init__(self, albedo: "Color") -> None:
        self.albedo = albedo

    def scatter(self, r_in: Ray, rec: HitRecord) -> Tuple[bool | Color | Ray]:
        reflected = self._reflect(r_in.direction(), rec.normal)
        return True, self.albedo, Ray(rec.p, reflected)
    
    def _reflect(self, v: "Vector3", n: "Vector3") -> "Vector3":
        return v - 2 * v.dot(n) * n
    