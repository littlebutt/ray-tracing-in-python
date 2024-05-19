from vec import Point3, Vector3


__all__ = ['Ray']


class Ray:
    '''
    A class modeling a ray.
    The equation of the ray is R(t) = orig + dir * t, where orig is the
    :class:`Point3` origin and dir is :class:`Vector3` direction.

    Attributes:
        orig: The origin point of the ray.
        dir: The direction of the ray.

    '''

    def __init__(self, orig: "Point3" = Point3(),
                 dir: "Vector3" = Vector3()) -> None:
        self.orig = orig
        self.dir = dir

    def origin(self) -> "Point3":
        return self.orig

    def direction(self) -> "Vector3":
        return self.dir

    def at(self, t: float) -> "Point3":
        '''
        Calculate the hit point with the given :args:`t`.

        '''
        return self.orig + self.dir * t
