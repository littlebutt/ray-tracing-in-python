import functools
from random import randint
from typing import List, Optional, Tuple
from aabb import AABB
from world import World
from hittable import HitRecord
from interval import Interval
from ray import Ray
from hittable import Hittable


class BVHNode(Hittable):

    def __init__(self, objects: List["Hittable"]=list(), start: int=0, end: int=0,
                 world: "World"=None) -> None:
        if world is not None:
            objects = world.objects
            start = 0
            end = len(objects)

        axis = randint(0, 2)
        comparator = self.box_x_compare if axis == 0 else self.box_y_compare if axis == 1 else self.box_z_compare
        object_span = end - start
        if object_span == 1:
            self.left = objects[start]
            self.right = objects[start]
        elif object_span == 2:
            self.left = objects[start]
            self.right = objects[start + 1]
        else:
            objects[start:end].sort(key=functools.cmp_to_key(comparator))
            mid = int(start + object_span / 2)
            self.left = BVHNode(objects=objects, start=start, end=mid)
            self.right = BVHNode(objects=objects, start=mid, end=end)

        self.bbox = AABB(box0=self.left.bounding_box(), box1=self.right.bounding_box())
    
    @staticmethod
    def box_x_compare(a: "Hittable", b: "Hittable") -> bool:
        a_axis_interval = a.bounding_box().axis_interval(0)
        b_axis_interval = b.bounding_box().axis_interval(0)
        return a_axis_interval.min - b_axis_interval.min
    
    @staticmethod
    def box_y_compare(a: "Hittable", b: "Hittable") -> bool:
        a_axis_interval = a.bounding_box().axis_interval(1)
        b_axis_interval = b.bounding_box().axis_interval(1)
        return a_axis_interval.min - b_axis_interval.min
    
    @staticmethod
    def box_z_compare(a: "Hittable", b: "Hittable") -> bool:
        a_axis_interval = a.bounding_box().axis_interval(2)
        b_axis_interval = b.bounding_box().axis_interval(2)
        return a_axis_interval.min - b_axis_interval.min

    def hit(self, ray: Ray, interval: Interval) -> Tuple[bool, Optional["HitRecord"]]:
        if not self.bbox.hit(ray, interval):
            return False, None
        hit_left, rec_left = self.left.hit(ray, interval)
        hit_right, rec_right = self.right.hit(ray, Interval(interval.min, rec_left.t if rec_left is not None else interval.max))
        hit = hit_left or hit_right
        # FIXME: rearrange here
        rec = rec_right if rec_right is not None else rec_left
        return hit, rec
    
    def bounding_box(self) -> "AABB":
        return self.bbox