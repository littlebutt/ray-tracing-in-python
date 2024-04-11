from camera import Camera
from material import Lambertian, Metal
from sphere import Sphere
from vec import Color, Point3
from world import World


if __name__ == '__main__':
    aspect_ratio = 16.0 / 9.0

    image_width = 400

    samples_per_pixel = 100

    material_ground = Lambertian(Color(0.8, 0.8, 0.0))
    material_center = Lambertian(Color(0.1, 0.2, 0.5))
    material_left = Metal(Color(0.8, 0.8, 0.8), 0.3)
    material_right = Metal(Color(0.8, 0.6, 0.2))
    
    world = World()
    world.add(Sphere(Point3(0.0, -100.5, -1.0), 100.0, material_ground))
    world.add(Sphere(Point3(0.0, 0.0, -1.2), 0.5, material_center))
    world.add(Sphere(Point3(-1.0, 0.0, -1.0), 0.5, material_left))
    world.add(Sphere(Point3(1.0, 0.0, -1.2), 0.5, material_right))

    cam = Camera(aspect_ratio, image_width, samples_per_pixel, 50)
    cam.render(world, open("output.ppm", "w"))

    