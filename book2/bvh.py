import functools
from typing import List, Optional, Tuple
from aabb import AABB
from world import World
from hittable import HitRecord
from interval import EMPTY, Interval
from ray import Ray
from hittable import Hittable


class BVHNode(Hittable):

    def __init__(self, objects: List["Hittable"]=list(), start: int=0, end: int=0,
                 world: "World"=None) -> None:
        if world is not None:
            objects = world.objects
            start = 0
            end = len(objects)
        
        self.bbox = AABB(x=EMPTY, y=EMPTY, z=EMPTY)
        for object_index in range(start, end):
            self.bbox = AABB(box0=self.bbox, box1=objects[object_index].bounding_box())
        
        axis = self.bbox.longest_axis()
        comparator = self.box_x_compare if axis == 0 else self.box_y_compare if axis == 1 else self.box_z_compare
        object_span = end - start
        if object_span == 1:
            self.left = objects[start]
            self.right = objects[start]
        elif object_span == 2:
            self.left = objects[start]
            self.right = objects[start + 1]
        else:
            objects[start:end] = sorted(objects[start:end], key=functools.cmp_to_key(comparator))
            mid = int(start + object_span / 2)
            self.left = BVHNode(objects=objects, start=start, end=mid)
            self.right = BVHNode(objects=objects, start=mid, end=end)
    
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
        hit_right, rec_right = self.right.hit(ray, interval)
        if hit_left and hit_right:
            if rec_left.t < rec_right.t:
                return True, rec_left
            else:
                return True, rec_right
        elif hit_left:
            return True, rec_left
        elif hit_right:
            return True, rec_right
        else:
            return False, None
    
    def bounding_box(self) -> "AABB":
        return self.bbox