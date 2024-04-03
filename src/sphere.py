import math
from typing import Optional, Tuple
from hittable import HitRecord, Hittable
from ray import Ray
from vec import Point3


class Sphere(Hittable):

    def __init__(self, center: "Point3", radius: float) -> None:
        self.center = center
        self.radius = radius
    
    def hit(self, ray: Ray, ray_tmin: float, ray_tmax: float) -> Tuple[bool, Optional[HitRecord]]:
        oc = ray.origin() - self.center
        a = ray.direction().length_squared()
        half_b = oc.dot(ray.direction())
        c = oc.length_squared() - self.radius * self.radius
        discriminant = half_b * half_b - a * c

        if discriminant < 0:
            return (False, None)
        
        sqrtd = math.sqrt(discriminant)
        root = (-half_b - sqrtd) / a
        if root <= ray_tmin or root >= ray_tmax:
            root = (-half_b + sqrtd) / a
            if root <= ray_tmin or root >= ray_tmax:
                return (False, None)
        
        rec = HitRecord()
        rec.t = root
        rec.p = ray.at(rec.t)
        outward_normal = (rec.p - self.center) / self.radius
        rec.set_face_normal(ray=ray, outward_normal=outward_normal)

        return (True, rec)
