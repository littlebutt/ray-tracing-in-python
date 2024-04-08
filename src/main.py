from camera import Camera
from sphere import Sphere
from vec import Point3
from world import World


if __name__ == '__main__':
    aspect_ratio = 16.0 / 9.0

    image_width = 400

    samples_per_pixel = 100
    
    world = World()
    world.add(Sphere(Point3(0, 0, -1), 0.5))
    world.add(Sphere(Point3(0, -0.5, -1), 0.5))

    cam = Camera(aspect_ratio, image_width, samples_per_pixel)
    cam.render(world)

    