from typing import Any, Optional, Tuple
from interval import Interval
from ray import Ray
from vec import Point3, Vector3


__all__ = ['HitRecord', 'Hittable']


class HitRecord:

    # XXX: The type of :args:`mat` is :class:`Material`. We use :type:`Any` here
    # is avoiding circular import.
    def __init__(self, p: "Point3"=Point3(), normal: "Vector3"=Vector3(), t: float=0.0, front_face: bool = True, mat: Any=None) -> None:
        self.p = p
        self.normal = normal
        self.t = t
        self.front_face = front_face
        self.mat = mat
    
    def set_face_normal(self, ray: "Ray", outward_normal: "Vector3") -> None:
        front_face = ray.direction().dot(outward_normal)
        self.normal = outward_normal if front_face < 0 else -outward_normal



class Hittable:

    def hit(self, ray: "Ray", interval: "Interval") -> Tuple[bool, Optional["HitRecord"]]:
        pass