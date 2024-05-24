from typing import Optional
from constants import INFINITY


__all__ = ['Interval', 'EMPTY', 'UNIVERSE']


class Interval:
    '''
    Util class for detecting the relation between the target and two
    :type:`int`.

    Attributes:
        min: The minimum float.
        max: The maximum float.
        a: One of :class:`Interval`s when it is made up by two
            :class:`Intervals`.
        b: Another :class:`Interval`.
    '''

    def __init__(self, min: float = -INFINITY, max: float = INFINITY,
                 a: Optional["Interval"] = None,
                 b: Optional["Interval"] = None) -> None:
        self.min = min
        self.max = max
        # NOTE: `a` and `b` will cover the `min` and `max` if both
        # assigned. Use dict parameters if you want to pass to `a` and `b`.
        if a is not None and b is not None:
            self.min = a.min if a.min < b.min else b.min
            self.max = a.max if a.max > b.max else b.max

    def size(self) -> float:
        '''The difference between the :arg:`max` and the :arg:`min`.'''
        return self.max - self.min

    def contains(self, x: float) -> bool:
        '''
        Detect if the target is in the :class:`Interval` with edges included.

        Args:
            x: The target.

        '''
        return x >= self.min and x <= self.max

    def surrounds(self, x: float) -> bool:
        '''
        Detect if the target is out of the :class:`Interval` with edges
        excluded.

        Args:
            x: The target.

        '''
        return x > self.min and x < self.max

    def clamp(self, x: float) -> float:
        '''
        Return the clamped value of the target within the :class:`Interval`.

        Args:
            x: The target.

        '''
        if x < self.min:
            return self.min
        elif x > self.max:
            return self.max
        else:
            return x

    def expand(self, delta: float) -> "Interval":
        padding = delta / 2
        return Interval(self.min - padding, self.max + padding)


EMPTY = Interval(+INFINITY, -INFINITY)


UNIVERSE = Interval(-INFINITY, +INFINITY)
