from typing import List, Tuple
from aabb import AABB
from hittable import HitRecord, Hittable
from interval import Interval
from ray import Ray


__all__ = ['World']


class World(Hittable):
    '''
    A class for rendering the world.
    It is merely a list of :class:`Hittable`s.

    Attributes:
        objects: The list of :class:`Hittable` objects for rendering.
        bbox: The bounding box of the whole system.

    '''

    def __init__(self, object: "Hittable" = None) -> None:
        self.objects: List["Hittable"] = list()
        self.bbox = None
        if object is not None:
            self.add(object)

    def add(self, obj: "Hittable") -> None:
        ''' Add a hittable object. '''
        self.objects.append(obj)
        if self.bbox is None:
            self.bbox = obj.bounding_box()
        else:
            self.bbox = AABB(box0=self.bbox, box1=obj.bounding_box())

    def clear(self) -> None:
        self.objects.clear()

    def hit(self, ray: Ray, interval: "Interval") -> \
            Tuple[bool, HitRecord | None]:
        '''Detect if the objects in the world are hittable respectively.'''
        hit_anything = False
        return_rec = None
        closest_so_far = interval.max

        for obj in self.objects:
            hit, rec = obj.hit(ray, Interval(interval.min, closest_so_far))
            if hit:
                hit_anything = True
                closest_so_far = rec.t
                return_rec = rec

        return (hit_anything, return_rec)

    def bounding_box(self) -> AABB:
        return self.bbox
