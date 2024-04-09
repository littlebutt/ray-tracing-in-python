from math import sqrt
import random
from typing import TextIO
from constants import PI
from interval import Interval
from vec import Color, Vector3


def degrees_to_radians(degrees: float):
    return degrees * PI / 180.0


def random_float(min: float=0, max: float=1) -> float:
    return min + random.random() * (max - min)


def random_vector(min: float=0, max: float=1) -> "Vector3":
    return Vector3(random_float(min, max), random_float(min, max), random_float(min, max))
    

def random_in_unit_sphere() -> "Vector3":
    while True:
        p = random_vector(-1, 1)
        if p.length_squared() < 1:
            return p
    

def random_unit_vector() -> "Vector3":
    return random_in_unit_sphere().unit_vector()


def random_on_hemisphere(normal: "Vector3") -> "Vector3":
    on_unit_sphere = random_unit_vector()
    if on_unit_sphere.dot(normal) > 0.0:
        return on_unit_sphere
    else:
        return - on_unit_sphere
    

def linear_to_gamma(linear_component: float) -> float:
    if linear_component > 0:
        return sqrt(linear_component)
    return 0


def write_color(text_io: TextIO, pixel_color: Color) -> None:
    r = linear_to_gamma(pixel_color.x)
    g = linear_to_gamma(pixel_color.y)
    b = linear_to_gamma(pixel_color.z)
    intensity = Interval(0.000, 0.999)
    rbyte = int(256 * intensity.clamp(r))
    gbyte = int(256 * intensity.clamp(g))
    bbyte = int(256 * intensity.clamp(b))
    text_io.write(f"{rbyte} {gbyte} {bbyte}\n")