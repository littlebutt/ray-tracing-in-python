import math
from typing import TextIO, Union

from interval import Interval


__all__ = ['Vector3', 'Point3', 'write_color']


class Vector3:

    def __init__(self, x: float=0, y: float=0, z: float=0) -> None:
        self.x = x
        self.y = y
        self.z = z
    
    def __neg__(self) -> "Vector3":
        return Vector3(-self.x, -self.y, -self.z)
    
    def __getitem__(self, key: int) -> float:
        if key == 0:
            return self.x
        elif key == 1:
            return self.y
        elif key == 2:
            return self.z
        else:
            raise IndexError("Index out of bound")
    
    def __add__(self, vector3: "Vector3") -> "Vector3":
        return Vector3(
            self.x + vector3.x,
            self.y + vector3.y,
            self.z + vector3.z
        )

    def __iadd__(self, vector3: "Vector3") -> "Vector3":
        return Vector3(
            self.x + vector3.x,
            self.y + vector3.y,
            self.z + vector3.z
        )
    
    def __sub__(self, vector3: "Vector3") -> "Vector3":
        return Vector3(
            self.x - vector3.x,
            self.y - vector3.y,
            self.z - vector3.z
        )
    
    def __mul__(self, other: Union["Vector3", float]) -> "Vector3":
        if isinstance(other, Vector3):
            return Vector3(
                self.x * other.x,
                self.y * other.y,
                self.z * other.z
            )
        else:
            return Vector3(
                self.x * other,
                self.y * other,
                self.z * other
            )
    
    def __rmul__(self, other: float) -> "Vector3":
        return Vector3(
            self.x * other,
            self.y * other,
            self.z * other
        )
    
    def __imul__(self, other: float) -> "Vector3":
        return Vector3(
            self.x * other,
            self.y * other,
            self.z * other
        )
    
    def __truediv__(self, other: float) -> "Vector3":
        return Vector3(
            self.x / other,
            self.y / other,
            self.z / other
        )
    
    def __itruediv__(self, other: float) -> "Vector3":
        return self.__imul__(1/other)
    
    def dot(self, vector3: "Vector3") -> float:
        return self.x * vector3.x + self.y * vector3.y + self.z * vector3.z
    
    def cross(self, vector3: "Vector3") -> "Vector3":
        return Vector3(self.y * vector3.z - self.z * vector3.y,
                self.z * vector3.x - self.x * vector3.z,
                self.x * vector3.y - self.y * vector3.x)
    
    def unit_vector(self) -> "Vector3":
        return self / self.length()
    
    def length_squared(self) -> float:
        return self.x * self.x + self.y * self.y + self.z * self.z
    
    def length(self) -> float:
        return math.sqrt(self.length_squared())
    
    def __repr__(self) -> str:
        return f"Vector3({self.x}, {self.y}, {self.z})"
    

Point3 = Vector3


Color = Vector3

def write_color(text_io: TextIO, pixel_color: Color) -> None:
    r = pixel_color.x
    g = pixel_color.y
    b = pixel_color.z
    intensity = Interval(0.000, 0.999)
    rbyte = int(256 * intensity.clamp(r))
    gbyte = int(256 * intensity.clamp(g))
    bbyte = int(256 * intensity.clamp(b))
    text_io.write(f"{rbyte} {gbyte} {bbyte}\n")