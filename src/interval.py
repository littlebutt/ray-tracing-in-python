from constants import INFINITY


__all__ = ['Interval', 'EMPTY', 'UNIVERSE']


class Interval:

    def __init__(self, min: float=-INFINITY, max: float=INFINITY) -> None:
        self.min = min
        self.max = max
    
    def contains(self, x: float) -> bool:
        return x >= self.min and x <= self.max
    
    def surrounds(self, x: float) -> bool:
        return x > self.min and x < self.max

EMPTY = Interval(+INFINITY, -INFINITY)
UNIVERSE = Interval(-INFINITY, +INFINITY)