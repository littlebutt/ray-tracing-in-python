from quad import Quad
from tex import CheckerTexture, ImageTexture, NoiseTexture
from bvh import BVHNode
from utils import random_float
from camera import Camera
from material import Lambertian
from sphere import Sphere
from vec import Color, Point3, Vector3
from world import World


if __name__ == '__main__':
    aspect_ratio = 16.0 / 9.0

    image_width = 400

    samples_per_pixel = 100

    checker = CheckerTexture(0.32, c1=Color(0.2, 0.3, 0.1), c2=Color(0.9, 0.9, 0.9))
    earth = ImageTexture(filename="earthmap.jpg")
    perlin = NoiseTexture(4)

    material_ground = Lambertian(Color(0.2, 0.8, 0.8))
    material_checker = Lambertian(texture=checker)
    material_earth = Lambertian(texture=earth)
    material_perlin = Lambertian(texture=perlin)
    
    world = World()
    world.add(Sphere(Point3(0.0, -100.5, -1.0), 100.0, material_ground))
    center = Point3(0.0, 0.0, -1.2) + Vector3(0, random_float(0, 0.1), 0)
    world.add(Quad(Point3(-3, -2, 5), Vector3(0, 0, -4), Vector3(0, 4, 0), Lambertian(Color(1, 0.2, 0.2))))

    world = World(BVHNode(world=world))

    cam = Camera(1.0, image_width, samples_per_pixel, 50, 80, Point3(-0, 0, 9), Point3(0, 0, 0), Vector3(0, 1, 0))
    cam.render(world, open("output6.ppm", "w"))

    