from sys import stdout
from constants import INFINITY
from interval import Interval
from ray import Ray
from utils import random_float
from vec import Color, Point3, Vector3, write_color
from world import World


class Camera:
    '''
    :class:`Camera` provides the APIs for rendering the graphic with the given 
    arguments.

    Attributes:
        aspect_ratio: Ratio of image width over height.
        image_width: Rendered image width in pixel count.
        image_height: Rendered image height.
        center: Camera center.
        pixel00_loc: Location of pixel 0, 0.
        pixel_delta_u: Offset to pixel to the right.
        pixel_delta_v: Offset to pixel below.
        samples_per_pixel: Count of random samples for each pixel.
        pixel_samples_scale: Color scale factor for a sum of pixel samples.

    '''

    def __init__(self, aspect_ratio: float=1.0, image_width: float=100, samples_per_pixel: float=10) -> None:
        self.aspect_ratio = aspect_ratio
        self.image_width = image_width
        self.samples_per_pixel = samples_per_pixel
    
    def render(self, world: "World"):
        self._initialize()
        stdout.write(f"P3\n{self.image_width} {self.image_height}\n255\n")
        for j in range(self.image_height):
            for i in range(self.image_width):
                pixel_color = Color(0, 0, 0)
                for sample in range(0, self.samples_per_pixel):
                    r = self._get_ray(i, j)
                    pixel_color += self._ray_color(r, world)
                write_color(stdout, self.pixel_samples_scale  * pixel_color)
    
    def _get_ray(self, i: int, j: int) -> "Ray":
        offset = self._sample_square()
        pixel_sample = self.pixel00_loc + ((i + offset.x) * self.pixel_delta_u) + ((j + offset.y) * self.pixel_delta_v)
        ray_origin = self.center
        ray_direction = pixel_sample - ray_origin
        return Ray(ray_origin, ray_direction)

    def _sample_square(self) -> "Vector3":
        return Vector3(random_float() - 0.5, random_float() - 0.5, 0)

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

        self.pixel_samples_scale = 1.0 / self.samples_per_pixel

    def _ray_color(self, ray: "Ray", world: "World") -> "Color":
        rec = None
        hit, rec = world.hit(ray, Interval(0, INFINITY))
        if hit:
            return 0.5 * (rec.normal + Color(1, 1, 1))
        unit_direction = ray.direction().unit_vector()
        a = 0.5 * (unit_direction.y + 1.0)
        return (1.0 - a) * Color(1.0, 1.0, 1.0) + a * Color(0.5, 0.7, 1.0)