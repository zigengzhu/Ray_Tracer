import time
import numpy as np
import torch
import sys
import rtxUtil as ru
from hittable import HittableList
from sphere import Sphere
from camera import Camera
from material import Material, Lambertian, Metal, Dielectric, DiffuseLight
from rectangle import XZRectangle, YZRectangle, XYRectangle
from bvh import BVHNode


class Scene:
    output_path: str
    img_width: int
    img_height: int
    samples_per_pixel: int
    max_depth: int

    world: HittableList
    camera: Camera

    background = np.array([0.0, 0.0, 0.0])

    lookfrom: np.array
    lookat: np.array

    vup = np.array([0.0, 1.0, 0.0])
    vfov = 40.0
    aperature = 0.0
    focus_dist = 10.0

    def __init__(self, output_path: str, img_width: int, img_height: int, samples_per_pixel: int, max_depth: int,
                 setting: str):
        if img_width > 1 and img_height > 1 and samples_per_pixel > 0 and max_depth > 0:
            print("\nPath:", " " * 14, output_path)
            print("Width:", " " * 13, img_width, "px")
            print("Height:", " " * 12, img_height, "px")
            print("Samples per pixel:  ", samples_per_pixel)
            print("Max Depth:", " " * 9, max_depth)
        else:
            print("Invalid output size.")
            exit(-1)

        self.output_path = output_path

        self.img_width = img_width
        self.img_height = img_height
        self.samples_per_pixel = samples_per_pixel
        self.max_depth = max_depth

        self.world = HittableList()

        if setting == "cornell_box":
            self.cornell_box()
        elif setting == "random_spheres":
            self.random_spheres()
        elif setting == "basic":
            self.basic()

    def render(self):
        start = time.time()
        f = open(self.output_path, "w")
        f.write("P3\n")
        f.write("# " + self.output_path + "\n")
        f.write("# Ray Tracer created by Zigeng Zhu (zigeng2@illinois.edu)\n")
        f.write(str(self.img_width) + " " + str(self.img_height) + "\n255\n")

        temp = 0
        for j in range(self.img_height - 1, -1, -1):
            # Print real time render progress in-line
            progress = int(100 - 100 * j / self.img_height)
            if progress % 5 == 0 and progress != temp:
                temp = progress
                print('Progress: %d%%' % temp, end='\r', flush=True)

            for i in range(0, self.img_width):
                pixel_color = np.array([0, 0, 0], dtype=float)
                for _ in range(0, self.samples_per_pixel):
                    u = (i + ru.get_random()) / (self.img_width - 1)
                    v = (j + ru.get_random()) / (self.img_height - 1)
                    pixel_color += ru.ray_color(self.camera.get_ray(u, v), self.background, self.world, self.max_depth)
                f.write(ru.color_to_str(pixel_color, self.samples_per_pixel))

        f.close()
        end = time.time()
        print("\nRender complete.\n")
        print("(normal) Time taken: " + str(end - start) + '\n')

    def cornell_box(self):
        self.lookfrom = np.array([278, 278, -800])
        self.lookat = np.array([278, 278, 0])

        self.camera = Camera(self.img_width, self.img_height, self.lookfrom, self.lookat, self.vup, self.vfov,
                             self.aperature, self.focus_dist)

        red = Lambertian(np.array([0.65, 0.05, 0.05]))
        white = Lambertian(np.array([0.73, 0.73, 0.73]))
        green = Lambertian(np.array([0.12, 0.45, 0.15]))
        light = DiffuseLight(np.array([15, 15, 15]))

        self.world.add(YZRectangle(0, 555, 0, 555, 555, green))
        self.world.add(YZRectangle(0, 555, 0, 555, 0, red))
        self.world.add(XZRectangle(213, 343, 227, 332, 554, light))
        self.world.add(XZRectangle(0, 555, 0, 555, 0, white))
        self.world.add(XZRectangle(0, 555, 0, 555, 555, white))
        self.world.add(XYRectangle(0, 555, 0, 555, 555, white))

        self.world.add(BVHNode(self.world.objects, 0, len(self.world.objects), 0, 1))

    def random_spheres(self):
        self.lookfrom = np.array([13.0, 2.0, 3.0])
        self.lookat = np.array([0.0, 0.0, 0.0])
        self.vfov = 20.0
        self.aperature = 0.1
        self.background = np.array([0.7, 0.8, 1.0])

        self.camera = Camera(self.img_width, self.img_height, self.lookfrom, self.lookat, self.vup, self.vfov,
                             self.aperature, self.focus_dist)

        mat_ground = Lambertian(np.array([0.5, 0.5, 0.5]))
        self.world.add(Sphere(np.array([0.0, -1000, 0.0]), 1000, mat_ground))

        for a in range(-11, 11):
            for b in range(-11, 11):
                choose_mat = ru.get_random()
                center = np.array([a + 0.9 * ru.get_random(), 0.2, b + 0.9 * ru.get_random()])

                if ru.length(center - np.array([4.0, 0.2, 0.0])) > 0.9:
                    sphere_material: Material
                    if choose_mat < 0.8:
                        albedo = ru.get_random_point() * ru.get_random_point()
                        sphere_material = Lambertian(albedo)
                    elif choose_mat < 0.95:
                        albedo = ru.get_random_point_in_range(0.5, 1.0)
                        fuzz = ru.get_random_in_range(0.0, 0.5)
                        sphere_material = Metal(albedo, fuzz)
                    else:
                        sphere_material = Dielectric(1.5)
                    self.world.add(Sphere(center, 0.2, sphere_material))

        mat1 = Dielectric(1.5)
        self.world.add(Sphere(np.array([0.0, 1.0, 0.0]), 1.0, mat1))

        mat2 = Lambertian(np.array([0.4, 0.2, 0.1]))
        self.world.add(Sphere(np.array([-4.0, 1.0, 0.0]), 1.0, mat2))

        mat3 = Metal(np.array([0.7, 0.6, 0.5]), 0.0)
        self.world.add(Sphere(np.array([4.0, 1.0, 0.0]), 1.0, mat3))

        # BVH implementation
        self.world.add(BVHNode(self.world.objects, 0, len(self.world.objects), 0, 1))

    def basic(self):
        self.lookfrom = np.array([3.0, 3.0, 2.0])
        self.lookat = np.array([0.0, 0.0, -1.0])
        self.vup = np.array([0.0, 1.0, 0.0])
        self.vfov = 20.0
        #self.aperature = 2.0
        #self.focus_dist = ru.length(self.lookfrom - self.lookat)


        self.camera = Camera(self.img_width, self.img_height, self.lookfrom, self.lookat, self.vup, self.vfov,
                             self.aperature, self.focus_dist)

        mat_ground = Lambertian(np.array([0.8, 0.8, 0.0]))
        mat_center = Lambertian(np.array([0.1, 0.2, 0.5]))
        mat_left = Dielectric(1.5)
        mat_right = Metal(np.array([0.8, 0.6, 0.2]), 0.0)

        self.world.add(Sphere(np.array([0.0, -100.5, -1.0]), 100, mat_ground))
        self.world.add(Sphere(np.array([0.0, 0.0, -1.0]), 0.5, mat_center))
        self.world.add(Sphere(np.array([-1.0, 0.0, -1.0]), 0.5, mat_left))
        self.world.add(Sphere(np.array([-1.0, 0.0, -1.0]), -0.45, mat_left))
        self.world.add(Sphere(np.array([1.0, 0.0, -1.0]), 0.5, mat_right))

        self.world.add(BVHNode(self.world.objects, 0, len(self.world.objects), 0, 1))
        self.background = np.array([0.7, 0.8, 1.0])
