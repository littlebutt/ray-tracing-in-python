from math import acos, atan2, sqrt
from typing import Optional, Tuple
from aabb import AABB
from constants import PI
from hittable import HitRecord, Hittable
from interval import Interval
from material import Material
from ray import Ray
from vec import Point3, Vector3


__all__ = ['Sphere']


class Sphere(Hittable):
    '''
    The sphere object for rendering.

    Attributes:
        center1: The center of the sphere.
        radius: The radius of the sphere.
        mat: The material of the sphere.
        center2: The other center of the sphere if it is bouncing at the
            highest point.
        is_moving: True if the sphere is moving. In this case :arg:`center2`
            is provided.
        center_vec: The vector pointing from :arg:`center1` to :arg:`center2`.
        bbox: The bounding box of the sphere.

    '''

    def __init__(self,
                 center1: "Point3",
                 radius: float,
                 mat: "Material" = Material(),
                 center2: Optional["Point3"] = None) -> None:
        self.center1 = center1
        self.radius = radius
        self.mat = mat

        rvec = Vector3(radius, radius, radius)

        if center2 is not None:
            self.is_moving = True
            self.center_vec = center2 - center1
            aabb1 = AABB(a=center1 - rvec, b=center1 + rvec)
            aabb2 = AABB(a=center2 - rvec, b=center2 + rvec)
            self.bbox = AABB(box0=aabb1, box1=aabb2)
        else:
            self.is_moving = False
            self.bbox = AABB(a=center1 - rvec, b=center1 + rvec)

    def sphere_center(self, time: float) -> "Point3":
        '''
        Return the center of the sphere according to the given :arg:`time`.

        '''
        # Linearly interpolate from center to center2 according to time, where
        # t=0 yields center, and t=1 yields center2.
        return self.center1 + time * self.center_vec

    def get_sphere_uv(self, p: "Point3", rec: "HitRecord"):
        '''
        Calculate the u and v pair for the texture.

        '''
        theta = acos(-p.y)
        phi = atan2(-p.z, p.x) + PI
        rec.u = phi / (2 * PI)
        rec.v = theta / PI

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
        self.center = self.sphere_center(ray.time()) \
            if self.is_moving else self.center1

        oc = ray.origin() - self.center
        a = ray.direction().length_squared()
        half_b = oc.dot(ray.direction())
        c = oc.length_squared() - self.radius * self.radius
        discriminant = half_b * half_b - a * c

        if discriminant < 0:
            return (False, None)

        sqrtd = sqrt(discriminant)
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
        self.get_sphere_uv(outward_normal, rec)
        rec.mat = self.mat

        return (True, rec)

    def bounding_box(self) -> AABB:
        return self.bbox
