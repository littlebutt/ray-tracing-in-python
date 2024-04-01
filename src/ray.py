from vec import Point3, Vector3


__all__ = ['Ray']


class Ray:

    def __init__(self, orig: "Point3"=Point3(), dir: "Vector3"=Vector3()) -> None:
        self.orig = orig
        self.dir = dir
    
    def origin(self) -> "Point3":
        return self.orig
    
    def direction(self) -> "Vector3":
        return self.dir
    
    def at(self, t: float) -> "Point3":
        return self.orig + self.dir * t
    