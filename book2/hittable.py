from typing import Any, Optional, Tuple
from aabb import AABB
from interval import Interval
from ray import Ray
from vec import Point3, Vector3


__all__ = ['HitRecord', 'Hittable']


class HitRecord:
    '''
    Record the information when the :class:`Ray` hit a :class:`Hittable`s.

    Attributes:
        p: The hit point in :class:`Point3` format.
        normal: The normal vector of the hit point in :class:`Point3` format.
        t: The parameter ``t`` in the ray equation.
        front_face: If the :args:`normal` points outward of the surface.
        mat: The :class:`Material` of the surface.

    '''

    # XXX: The type of :args:`mat` is :class:`Material`. We use :type:`Any` here
    # is avoiding circular import.
    def __init__(self, p: "Point3"=Point3(), normal: "Vector3"=Vector3(), t: float=0.0, front_face: bool = True, mat: Any=None) -> None:
        self.p = p
        self.normal = normal
        self.t = t
        self.front_face = front_face
        self.mat = mat
        self.u = 0
        self.v = 0
    
    def set_face_normal(self, ray: "Ray", outward_normal: "Vector3") -> None:
        '''Set the front face of the hit point.'''
        front_face = ray.direction().dot(outward_normal)
        self.normal = outward_normal if front_face < 0 else -outward_normal



class Hittable:

    def hit(self, ray: "Ray", interval: "Interval") -> Tuple[bool, Optional["HitRecord"]]:
        '''
        Detect if the :class:`Ray` can hit the target within the interval. If hittable, it will 
        return its :class:`HitRecord`.

        Args:
            ray: The ray equation for detecting.
            interval: The given :class:`Interval`.
        
        Returns:
            bool: If the ray can hit it.
            HitRecord: The :class:`HitRecord` of the hit point if hittable.

        '''
        pass

    def bounding_box(self) -> "AABB":
        pass