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

    world = World()
    material_ground = Lambertian(Color(0.5, 0.5, 0.5))  
    world.add(Sphere(Point3(0.0, -1000, 0), 1000, material_ground))

    for a in range(-6, 6):
        for b in range(-6, 6):
            choose_mat = random_float()
            center = Point3(a + 0.9 * random_float(), 0.2, b + 0.9 * random_float())

            if (center - Point3(4, 0.2, 0)).length() > 0.9:
                if choose_mat < 0.8:
                    albedo = random_vector() * random_vector()
                    material = Lambertian(albedo)
                    center2 = center + Vector3(0, random_float(0, 0.5), 0)
                    world.add(Sphere(center, 0.2, material, True, center2))
                elif choose_mat < 0.95:
                    albedo = random_vector(0.5, 1)
                    fuzz = random_float(0, 0.5)
                    material = Metal(albedo, fuzz)
                    world.add(Sphere(center, 0.2, material))
                else:
                    material = Dielectric(0.5)
                    world.add(Sphere(center, 0.2, material))


    cam = Camera(aspect_ratio=aspect_ratio, image_width=image_width, samples_per_pixel=samples_per_pixel, 
                 max_depth=50, vfov=20, 
                 look_from=Point3(13, 2, 3), look_at=Point3(0, 0, 0), vup=Vector3(0, 1, 0))
    cam.render(world, open("output.ppm", "w"))
    # aspect_ratio = 16.0 / 9.0

    # image_width = 400

    # samples_per_pixel = 100

    # material_ground = Lambertian(Color(0.8, 0.8, 0.0))
    # material_center = Lambertian(Color(0.1, 0.2, 0.5))
    # material_left = Dielectric(1.5)
    # material_right = Metal(Color(0.8, 0.6, 0.2))
    
    # world = World()
    # world.add(Sphere(Point3(0.0, -100.5, -1.0), 100.0, material_ground))
    # center = Point3(0.0, 0.0, -1.2) + Vector3(0, random_float(0, 0.5), 0)
    # world.add(Sphere(Point3(0.0, 0.0, -1.2), 0.5, material_center))
    # world.add(Sphere(Point3(-1.0, 0.0, -1.2), 0.5, material_left))
    # world.add(Sphere(Point3(1.0, 0.0, -1.2), 0.5, material_right))

    # cam = Camera(aspect_ratio, image_width, samples_per_pixel, 50, 20, Point3(-2, 2, 1), Point3(0, 0, -1), Vector3(0, 1, 0))
    # cam.render(world, open("output.ppm", "w"))

    