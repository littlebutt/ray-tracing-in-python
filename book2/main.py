from bvh import BVHNode
from utils import random_float, random_vector
from camera import Camera
from material import Dielectric, Lambertian, Metal
from sphere import Sphere
from vec import Color, Point3, Vector3
from world import World


if __name__ == '__main__':
    aspect_ratio = 16.0 / 9.0

    image_width = 400

    samples_per_pixel = 100

    material_ground = Lambertian(Color(0.2, 0.8, 0.8))
    material_center = Lambertian(Color(0.1, 0.2, 0.5))
    material_red = Lambertian(Color(0.8, 0.2, 0.2))
    material_green = Lambertian(Color(0.2, 0.8, 0.2))
    material_yellow = Lambertian(Color(0.8, 0.8, 0.2))
    
    world = World()
    world.add(Sphere(Point3(0.0, -100.5, -1.0), 100.0, material_ground))
    center = Point3(0.0, 0.0, -1.2) + Vector3(0, random_float(0, 0.1), 0)
    world.add(Sphere(Point3(0.0, 0.001, -1.2), 0.5, material_center, center))
    # world.add(Sphere(Point3(1.0, 0.002, -1.2), 0.7, material_red))
    # world.add(Sphere(Point3(-1.0, 0.003, -1.2), 0.5, material_green))
    # world.add(Sphere(Point3(1.0, 0.004, -1.2), 0.5, material_yellow))

    world = World(BVHNode(world=world))

    cam = Camera(aspect_ratio, image_width, samples_per_pixel, 50, 20, Point3(-2, 2, 1), Point3(0, 0, -1), Vector3(0, 1, 0))
    cam.render(world, open("output2.ppm", "w"))

    