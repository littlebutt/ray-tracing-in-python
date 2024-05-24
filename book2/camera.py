from math import tan
from typing import TextIO
from constants import INFINITY
from interval import Interval
from ray import Ray
from utils import degrees_to_radians, random_float, write_color
from vec import Color, Point3, Vector3
from world import World


__all__ = ['Camera']


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
        max_depth: Maximum number of ray bounces into scene.
        vfov: Vertical view angle (field of view).
        look_from: Point camera is looking from.
        look_at: Point camera is looking at.
        vup: Camera-relative "up" direction.
        background: The background color of the image when we do diffuse light
            rendering.

    '''

    def __init__(self,
                 aspect_ratio: float = 1.0,
                 image_width: float = 100,
                 samples_per_pixel: float = 10,
                 max_depth: int = 10,
                 vfov: float = 90,
                 look_from: "Point3" = Point3(0, 0, 0),
                 look_at: "Point3" = Point3(0, 0, -1),
                 vup: "Vector3" = Vector3(0, 1, 0),
                 background: "Color" = Color(0, 0, 0)) -> None:

        self.aspect_ratio = aspect_ratio
        self.image_width = image_width
        self.samples_per_pixel = samples_per_pixel
        self.max_depth = max_depth
        self.vfov = vfov
        self.look_from = look_from
        self.look_at = look_at
        self.vup = vup
        self.background = background

    def render(self, world: "World", out: TextIO):
        '''
        Render the image of the ray tracing model.
        The result of the rendering process is a ``.ppm`` image from the output
        stream.

        Arguments:
            world: The hittable objects for rendering.
            out: The :type:`TextIO` output stream.
        '''
        self._initialize()
        print(f"Start to render the image. The total batch number is "
              f"{self.image_height * self.image_width}")
        out.write(f"P3\n{self.image_width} {self.image_height}\n255\n")
        for j in range(self.image_height):
            for i in range(self.image_width):
                pixel_color = Color(0, 0, 0)
                print(f"Rendering the {i + j * self.image_height}/"
                      f"{self.image_height * self.image_width} batch")
                for sample in range(0, self.samples_per_pixel):
                    r = self._get_ray(i, j)
                    pixel_color += self._ray_color(r, self.max_depth, world)
                write_color(out, self.pixel_samples_scale * pixel_color)
        out.flush()

    def _get_ray(self, i: int, j: int) -> "Ray":
        offset = self._sample_square()
        pixel_sample = self.pixel00_loc + \
            ((i + offset.x) * self.pixel_delta_u) + \
            ((j + offset.y) * self.pixel_delta_v)
        ray_origin = self.center
        ray_direction = pixel_sample - ray_origin
        ray_time = random_float()
        return Ray(ray_origin, ray_direction, ray_time)

    def _sample_square(self) -> "Vector3":
        return Vector3(random_float() - 0.5, random_float() - 0.5, 0)

    def _initialize(self):
        self.image_height = int(self.image_width / self.aspect_ratio)
        self.image_height = self.image_height if self.image_height > 1 else 1

        self.focal_length = (self.look_from - self.look_at).length()
        theta = degrees_to_radians(self.vfov)
        h = tan(theta / 2)
        self.viewport_height = 2.0 * h * self.focal_length
        self.viewport_width = self.viewport_height * \
            float(self.image_width / self.image_height)

        self.center = self.look_from

        w = (self.look_from - self.look_at).unit_vector()
        u = self.vup.cross(w).unit_vector()
        v = w.cross(u)

        self.viewport_u = self.viewport_width * u
        self.viewport_v = self.viewport_height * -v

        self.pixel_delta_u = self.viewport_u / self.image_width
        self.pixel_delta_v = self.viewport_v / self.image_height

        self.viewport_upper_left = self.center - self.focal_length * w - \
            self.viewport_u / 2 - self.viewport_v / 2

        self.pixel00_loc = self.viewport_upper_left + 0.5 * \
            (self.pixel_delta_u + self.pixel_delta_v)

        self.pixel_samples_scale = 1.0 / self.samples_per_pixel

    def _ray_color(self, ray: "Ray", depth: int, world: "World") -> "Color":
        if depth <= 0:
            return Color(0, 0, 0)

        hit, rec = world.hit(ray, Interval(0.001, INFINITY))
        if not hit:
            return self.background

        color_from_emission = rec.mat.emitted(rec.u, rec.v, rec.p)

        res, attenuation, scattered = rec.mat.scatter(ray, rec)
        if not res:
            return color_from_emission

        color_from_scatter = attenuation * \
            self._ray_color(scattered, depth - 1, world)
        return color_from_emission + color_from_scatter
