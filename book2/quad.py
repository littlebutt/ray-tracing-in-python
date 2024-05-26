from math import fabs
from typing import Tuple
from aabb import AABB
from hittable import HitRecord
from interval import Interval
from ray import Ray
from material import Material
from vec import Point3, Vector3
from hittable import Hittable


class Quad(Hittable):

    def __init__(self, q: "Point3", u: "Vector3", v: "Vector3",
                 mat: "Material" = Material()) -> None:
        self.q = q
        self.u = u
        self.v = v
        self.mat = mat

        n = self.u.cross(self.v)
        self.normal = n.unit_vector()
        self.d = self.normal.dot(self.q)

        self.w = n / n.dot(n)

        self._set_bounding_box()

    def _set_bounding_box(self) -> None:
        bbox_diagnol1 = AABB(a=self.q, b=self.q+self.u+self.v)
        bbox_diagnol2 = AABB(a=self.q+self.u, b=self.q+self.v)
        self.bbox = AABB(box0=bbox_diagnol1, box1=bbox_diagnol2)

    def bounding_box(self) -> AABB:
        return self.bbox

    def hit(self, ray: Ray, interval: Interval) -> \
            Tuple[bool, HitRecord | None]:
        denom = self.normal.dot(ray.direction())
        if fabs(denom) < 1e-8:
            return False, None

        t = (self.d - self.normal.dot(ray.origin())) / denom
        if not interval.contains(t):
            return False, None

        intersection = ray.at(t)
        planar_hitpt_vector = intersection - self.q
        alpha = self.w.dot(planar_hitpt_vector.cross(self.v))
        beta = self.w.dot(self.u.cross(planar_hitpt_vector))

        res, rec = self._is_interior(alpha, beta)
        if not res:
            return False, None
        rec.t = t
        rec.p = intersection
        rec.mat = self.mat
        rec.set_face_normal(ray, self.normal)

        return True, rec

    @staticmethod
    def _is_interior(alpha: float, beta: float) -> Tuple[bool, "HitRecord"]:
        unit_interval = Interval(0, 1)
        if (not unit_interval.contains(alpha)) or \
                (not unit_interval.contains(beta)):
            return False, None
        rec = HitRecord()
        rec.u = alpha
        rec.v = beta
        return True, rec
