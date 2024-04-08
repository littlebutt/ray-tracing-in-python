import random
from constants import PI


def degrees_to_radians(degrees: float):
    return degrees * PI / 180.0


def random_float(min: float=0, max: float=1) -> float:
    return random.uniform(min, max)