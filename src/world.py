from typing import List, Tuple
from hittable import HitRecord, Hittable
from ray import Ray


class World(Hittable):

    def __init__(self) -> None:
        self.objects: List["Hittable"] = list()
    
    def add(self, obj: "Hittable") -> None:
        self.objects.append(obj)
    
    def clear(self) -> None:
        self.objects.clear()
    
    def hit(self, ray: Ray, ray_tmin: float, ray_tmax: float) -> Tuple[bool, HitRecord | None]:
        hit_anything = False
        return_rec = None
        closest_so_far = ray_tmax

        for obj in self.objects:
            hit, rec = obj.hit(ray, ray_tmin, closest_so_far)
            if hit:
                hit_anything = True
                closest_so_far = rec.t
                return_rec = rec
        
        return (hit_anything, return_rec)

