from math import sqrt
from sys import stdout
from camera import Camera
from constants import INFINITY, PI
from interval import Interval
from ray import Ray
from sphere import Sphere
from vec import Color, Point3, Vector3, write_color
from world import World


def degrees_to_radians(degrees: float):
    return degrees * PI / 180.0


def ray_color(ray: "Ray", world: "World") -> "Color":
    rec = None
    hit, rec = world.hit(ray, Interval(0, INFINITY))
    if hit:
        return 0.5 * (rec.normal + Color(1, 1, 1))
    unit_direction = ray.direction().unit_vector()
    a = 0.5 * (unit_direction.y + 1.0)
    return (1.0 - a) * Color(1.0, 1.0, 1.0) + a * Color(0.5, 0.7, 1.0)


def hit_sphere(center: "Point3", radius: float, ray: "Ray") -> float:
    oc = ray.origin() - center
    a = r.direction().length_squared()
    half_b = oc.dot(ray.direction())
    b = 2.0 * oc.dot(r.direction())
    c = oc.length_squared() - radius * radius
    discriminant = half_b * half_b - a * c
    
    if discriminant < 0:
        return -1.0
    else:
        return (-half_b - sqrt(discriminant)) / a


if __name__ == '__main__':
    aspect_ratio = 16.0 / 9.0

    image_width = 400
    
    world = World()
    world.add(Sphere(Point3(0, 0, -1), 0.5))
    world.add(Sphere(Point3(0, -0.5, -1), 0.5))

    cam = Camera(aspect_ratio, image_width)
    cam.render(world)

    