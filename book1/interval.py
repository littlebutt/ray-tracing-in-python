from constants import INFINITY


__all__ = ['Interval', 'EMPTY', 'UNIVERSE']


class Interval:
    '''
    Util class for detecting the relation between the target and two :type:`int`.

    Attributes:
        min: The minimum int.
        max: The maximum int.

    '''

    def __init__(self, min: float=-INFINITY, max: float=INFINITY) -> None:
        self.min = min
        self.max = max
    
    def contains(self, x: float) -> bool:
        '''
        Detect if the target is in the :class:`Interval` with edges included.

        Args:
            x: The target.

        '''
        return x >= self.min and x <= self.max
    
    def surrounds(self, x: float) -> bool:
        '''
        Detect if the target is out of the :class:`Interval` with edges excluded.

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


EMPTY = Interval(+INFINITY, -INFINITY)


UNIVERSE = Interval(-INFINITY, +INFINITY)