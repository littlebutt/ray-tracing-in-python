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


def write_color(text_io: TextIO, pixel_color: Color) -> None:
    r = pixel_color.x
    g = pixel_color.y
    b = pixel_color.z
    intensity = Interval(0.000, 0.999)
    rbyte = int(256 * intensity.clamp(r))
    gbyte = int(256 * intensity.clamp(g))
    bbyte = int(256 * intensity.clamp(b))
    text_io.write(f"{rbyte} {gbyte} {bbyte}\n")