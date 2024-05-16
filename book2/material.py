from math import sqrt
from typing import Tuple
from tex import SolidColor, Texture
from hittable import HitRecord
from ray import Ray
from utils import near_zero, random_float, random_unit_vector
from vec import Color, Vector3


__all__ = ['Material', 'Lambertian', 'Metal', 'Dielectric']


class Material:
    '''
    A Class for material attributes.

    '''

    def scatter(self, r_in: "Ray", rec: "HitRecord") -> Tuple[bool, "Color", "Ray"]:
        '''
        Scattering the :class:`Ray` according to its material attributes.

        Args:
            r_in: The :class:`Ray`.
            rec: The :class:`HitRecord` of the hit point.
        
        Returns:
            bool: If the ray can scatter color, otherwise scatter 
                ``Color(0, 0, 0)``.
            Color: The color of the scattered ray.
            Ray: The scattered ray.
        '''
        return False
    
    def _reflect(self, v: "Vector3", n: "Vector3") -> "Vector3":
        return v - 2 * v.dot(n) * n


class Lambertian(Material):

    def __init__(self, albedo: "Color"=None, texture: "Texture"=None) -> None:
        if albedo is not None:
            self.tex = SolidColor(albedo=albedo)
        elif texture is not None:
            self.tex = texture

    def scatter(self, r_in: Ray, rec: HitRecord) -> Tuple[bool | Color | Ray]:
        scatter_direction = rec.normal + random_unit_vector()
        if near_zero(scatter_direction):
            scatter_direction = rec.normal
        return True, self.tex.value(rec.u, rec.v, rec.p), Ray(rec.p, scatter_direction, r_in.time())


class Metal(Material):

    def __init__(self, albedo: "Color", fuzz: float = 0) -> None:
        self.albedo = albedo
        self.fuzz = fuzz if fuzz < 1 else 1

    def scatter(self, r_in: Ray, rec: HitRecord) -> Tuple[bool | Color | Ray]:
        reflected = self._reflect(r_in.direction(), rec.normal)
        reflected = reflected.unit_vector() + self.fuzz * random_unit_vector()
        scattered = Ray(rec.p, reflected, r_in.time())
        return scattered.direction().dot(rec.normal) > 0, self.albedo, scattered


class Dielectric(Material):

    def __init__(self, refraction_index: float) -> None:
        self.refraction_index = refraction_index

    def scatter(self, r_in: Ray, rec: HitRecord) -> Tuple[bool | Color | Ray]:
        ri = 1.0 / self.refraction_index if rec.front_face else self.refraction_index
        unit_direction = r_in.direction().unit_vector()
        cos_theta = min(rec.normal.dot(-unit_direction), 1.0)
        sin_theta = sqrt(1.0 - cos_theta * cos_theta)
        if ri * sin_theta > 1.0 or self._reflectance(cos_theta, ri) > random_float():
            direction = self._reflect(unit_direction, rec.normal)
        else:
            direction = self._refract(unit_direction, rec.normal, ri)
        return True, Color(1.0, 1.0, 1.0), Ray(rec.p, direction, r_in.time())
    
    def _refract(self, uv: "Vector3", n: "Vector3", etai_over_eta: float) -> "Vector3":
        cos_theta = min(n.dot(-uv), 1.0)
        r_out_prep = etai_over_eta * (uv + cos_theta * n)
        r_out_parallel = -sqrt(abs(1.0 - r_out_prep.length_squared())) * n
        return r_out_prep + r_out_parallel
    
    def _reflectance(self, cosine: float, refraction_index: float) -> float:
        r0 = (1 - refraction_index) / (1 + refraction_index)
        r0 = r0 * r0
        return r0 + (1 - r0) * pow((1 - cosine), 5)
    