from typing import Optional
from ray import Ray
from vec import Point3
from interval import Interval


__all__ = ["AABB"]


class AABB:
    '''
    Axis-aligned bounding box, or :class:`AABB`, is a way to test if the ray
    can intersect objects in higher speed. The key idea of :class:`AABB` is to
    wrap an object in a box and test if the box can be hit by the ray rather
    than the object itself.

    Attributes:
        x: The two sides of the box along X-axis.
        y: The two sides of the box along Y-axis.
        z: The two sides of the box along Z-axis.
        a: One of the diagonal points of the box. With two diagonal points we
            can define a bounding box.
        b: The opposite diagonal points of the box.
        box0: A sub-box of the box. With two sub-box we can define a box which
            can hold the two boxes.
        box1: The other sub-box of the box.

    '''
    def __init__(self,
                 x: Optional["Interval"] = None,
                 y: Optional["Interval"] = None,
                 z: Optional["Interval"] = None,
                 a: Optional["Point3"] = None,
                 b: Optional["Point3"] = None,
                 box0: Optional["AABB"] = None,
                 box1: Optional["AABB"] = None) -> None:
        if x is not None and y is not None and z is not None:
            self.x = x
            self.y = y
            self.z = z
        elif a is not None and b is not None:
            # Treat the two points a and b as extrema for the bounding box, so
            # we don't require a particular minimum/maximum coordinate order.
            self.x = Interval(a[0], b[0]) if a[0] <= b[0]\
                else Interval(b[0], a[0])
            self.y = Interval(a[1], b[1]) if a[1] <= b[1]\
                else Interval(b[1], a[1])
            self.z = Interval(a[2], b[2]) if a[2] <= b[2]\
                else Interval(b[2], a[2])
        elif box0 is not None and box1 is not None:
            self.x = Interval(a=box0.x, b=box1.x)
            self.y = Interval(a=box0.y, b=box1.y)
            self.z = Interval(a=box0.z, b=box1.z)
        else:
            self.x = Interval()
            self.y = Interval()
            self.z = Interval()
        self._pad_to_minimums()

    def axis_interval(self, n: int) -> "Interval":
        '''
        Find the axis :class:`Interval` respectly.

        Args:
            n: The index of axis Interval.

        Returns:
            Interval: The interval along the axis.

        '''
        match n:
            case 0:
                return self.x
            case 1:
                return self.y
            case 2:
                return self.z
            case _:
                raise IndexError("Bad Index")

    def hit(self, ray: "Ray", ray_t: "Interval") -> bool:
        '''
        Test if the given :class:`Ray` can hit the box.

        Args:
            ray: The :class:`Ray` to be tested.
            ray_t: The :class:`Interval` for the test range.

        Returns:
            bool: If the box can be hit by the ray.

        '''
        ray_origin = ray.origin()
        ray_dir = ray.direction()

        for axis in range(3):
            ax = self.axis_interval(axis)
            adinv = 1.0 / ray_dir[axis]

            t0 = (ax.min - ray_origin[axis]) * adinv
            t1 = (ax.max - ray_origin[axis]) * adinv

            if t0 < t1:
                if t0 > ray_t.min:
                    ray_t.min = t0
                if t1 < ray_t.max:
                    ray_t.max = t1
            else:
                if t1 > ray_t.min:
                    ray_t.min = t1
                if t0 < ray_t.max:
                    ray_t.max = t0

            if ray_t.max <= ray_t.min:
                return False

        return True

    def longest_axis(self) -> int:
        '''
        Find the longest axis.
        '''
        if self.x.size() > self.y.size():
            return 0 if self.x.size() > self.z.size() else 2
        else:
            return 1 if self.y.size() > self.z.size() else 2

    def _pad_to_minimums(self) -> None:
        delta = 0.0001
        if self.x.size() < delta:
            self.x = self.x.expand(delta)
        if self.y.size() < delta:
            self.y = self.y.expand(delta)
        if self.z.size() < delta:
            self.z = self.z.expand(delta)
