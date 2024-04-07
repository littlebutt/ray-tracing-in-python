from sys import stdout
from constants import INFINITY
from interval import Interval
from ray import Ray
from vec import Color, Point3, Vector3, write_color
from world import World


class Camera:

    def __init__(self, aspect_ratio: float=1.0, image_width: float=100) -> None:
        self.aspect_ratio = aspect_ratio
        self.image_width = image_width
    
    def render(self, world: "World"):
        self._initialize()
        print(f"P3\n{self.image_width} {self.image_height}\n255")
        for j in range(self.image_height):
            for i in range(self.image_width):
                pixel_center = self.pixel00_loc + i * self.pixel_delta_u + j * self.pixel_delta_v
                ray_direction = pixel_center - self.center
                r = Ray(self.center, ray_direction)
                pixel_color = self._ray_color(r, world)
                write_color(stdout, pixel_color)

    def _initialize(self):
        self.image_height = int(self.image_width / self.aspect_ratio)
        self.image_height = self.image_height if self.image_height > 1 else 1

        self.focal_length = 1.0
        self.viewport_height = 2.0
        self.viewport_width = self.viewport_height * float(self.image_width / self.image_height)

        self.center = Point3(0, 0, 0)

        self.viewport_u = Vector3(self.viewport_width, 0, 0)
        self.viewport_v = Vector3(0, -self.viewport_height, 0)

        self.pixel_delta_u = self.viewport_u / self.image_width
        self.pixel_delta_v = self.viewport_v / self.image_height

        self.viewport_upper_left = self.center - Vector3(0, 0, self.focal_length) - self.viewport_u / 2 - self.viewport_v / 2

        self.pixel00_loc = self.viewport_upper_left + 0.5 * (self.pixel_delta_u + self.pixel_delta_v)


    def _ray_color(self, ray: "Ray", world: "World") -> "Color":
        rec = None
        hit, rec = world.hit(ray, Interval(0, INFINITY))
        if hit:
            return 0.5 * (rec.normal + Color(1, 1, 1))
        unit_direction = ray.direction().unit_vector()
        a = 0.5 * (unit_direction.y + 1.0)
        return (1.0 - a) * Color(1.0, 1.0, 1.0) + a * Color(0.5, 0.7, 1.0)