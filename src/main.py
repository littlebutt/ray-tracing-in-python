from sys import stdout
from ray import Ray
from vec import Color, Point3, Vector3, write_color


def ray_color(ray: "Ray") -> "Color":
    if hit_sphere(Point3(0, 0, -5), 0.5, ray):
        return Color(1, 0, 0)
    unit_direction = ray.direction().unit_vector()
    a = 0.5 * (unit_direction.y + 1.0)
    return (1.0 - a) * Color(1.0, 1.0, 1.0) + a * Color(0.5, 0.7, 1.0)


def hit_sphere(center: "Point3", radius: float, ray: "Ray") -> bool:
    oc = ray.origin() - center
    a = r.direction().dot(r.direction())
    b = 2.0 * oc.dot(r.direction())
    c = oc.dot(oc) - radius * radius
    discriminant = b * b - 4 * a * c
    return discriminant >= 0


if __name__ == '__main__':
    aspect_ratio = 16.0 / 9.0

    image_width = 400
    image_height = int(image_width / aspect_ratio)
    image_height = image_height if image_height > 1 else 1

    focal_length = 1.0
    viewport_height = 2.0
    viewport_width = viewport_height * float(image_width / image_height)

    camera_center = Point3(0, 0, 0)

    viewport_u = Vector3(viewport_width, 0, 0)
    viewport_v = Vector3(0, -viewport_height, 0)

    pixel_delta_u = viewport_u / image_width
    pixel_delta_v = viewport_v / image_height

    viewport_upper_left = camera_center - Vector3(0, 0, focal_length) - viewport_u / 2 - viewport_v / 2

    pixel00_loc = viewport_upper_left + 0.5 * (pixel_delta_u + pixel_delta_v)

    print(f"P3\n{image_width} {image_height}\n255")
    for j in range(image_height):
        for i in range(image_width):
            pixel_center = pixel00_loc + i * pixel_delta_u + j * pixel_delta_v
            ray_direction = pixel_center - camera_center
            r = Ray(camera_center, ray_direction)
            pixel_color = ray_color(r)
            write_color(stdout, pixel_color)