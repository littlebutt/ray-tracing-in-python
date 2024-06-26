import math
from typing import Optional, Tuple
from hittable import HitRecord, Hittable
from interval import Interval
from material import Material
from ray import Ray
from vec import Point3


__all__ = ['Sphere']


class Sphere(Hittable):
    '''
    The sphere object for rendering.

    Attributes:
        center: The center of the sphere.
        radius: The radius of the sphere.
        mat: The material of the sphere.

    '''

    def __init__(self, center: "Point3", radius: float,
                 mat: "Material" = Material()) -> None:
        self.center = center
        self.radius = radius
        self.mat = mat

    def hit(self, ray: Ray, interval: "Interval") -> \
            Tuple[bool, Optional[HitRecord]]:
        '''
        Detect if the ray can hit the sphere within the given
        :class:`Interval`.

        Args:
            ray: The ray for detecting if it is hittable.
            interval: The detect region of the ray.

        Returns:
            :type:`bool`: If the ray can hit the sphere.
            :class:`HitRecord`: The :class:`HitRecord` of the hit detection if
                the ray can hit the sphere.

        '''
        oc = ray.origin() - self.center
        a = ray.direction().length_squared()
        half_b = oc.dot(ray.direction())
        c = oc.length_squared() - self.radius * self.radius
        discriminant = half_b * half_b - a * c

        if discriminant < 0:
            return (False, None)

        sqrtd = math.sqrt(discriminant)
        root = (-half_b - sqrtd) / a
        if not interval.surrounds(root):
            root = (-half_b + sqrtd) / a
            if not interval.surrounds(root):
                return (False, None)

        rec = HitRecord()
        rec.t = root
        rec.p = ray.at(rec.t)
        outward_normal = (rec.p - self.center) / self.radius
        rec.set_face_normal(ray=ray, outward_normal=outward_normal)
        rec.mat = self.mat

        return (True, rec)
