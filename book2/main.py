from quad import Quad
from tex import CheckerTexture, ImageTexture, NoiseTexture
from bvh import BVHNode
from utils import random_float
from camera import Camera
from material import DiffuseLight, Lambertian
from sphere import Sphere
from vec import Color, Point3, Vector3
from world import World


if __name__ == '__main__':
    aspect_ratio = 16.0 / 9.0

    image_width = 400

    samples_per_pixel = 100

    checker = CheckerTexture(0.32, c1=Color(0.2, 0.3, 0.1), c2=Color(0.9, 0.9, 0.9))
    # earth = ImageTexture(filename="earthmap.jpg")
    perlin = NoiseTexture(4)
    
    diff_light = DiffuseLight(emit=Color(4, 4, 4))
    material_ground = Lambertian(Color(0.2, 0.8, 0.8))
    material_checker = Lambertian(texture=checker)
    # material_earth = Lambertian(texture=earth)
    material_perlin = Lambertian(texture=perlin)

    world = World()
    # world.add(Sphere(Point3(0.0, -100.5, -1.0), 100.0, material_ground))
    center = Point3(0.0, 0.0, -1.2) + Vector3(0, random_float(0, 0.1), 0)
    world.add(Sphere(Point3(0.0, 2, -1.2), 2, material_checker))
    world.add(Quad(q=Point3(-2, 0, 5), u=Vector3(4, 0, 0), v=Vector3(0, 4, 0), mat=diff_light))


    world = World(BVHNode(world=world))

    cam = Camera(aspect_ratio, image_width, samples_per_pixel, 50, 20, Point3(26, 3, 6), Point3(0, 2, 0), Vector3(0, 1, 0), Color(0.0, 0.0, 0.0))
    cam.render(world, open("output7.ppm", "w"))
