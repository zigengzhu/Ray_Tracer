import time
import numpy as np
import torch
import sys
import rtxUtil as ru
from hittable import HittableList
from sphere import Sphere
from camera import Camera
from material import Material, Lambertian, Metal, Dielectric
from bvh import BVHNode


def linear_render():
    print("linear_render")
    start = time.time()
    temp = 0
    for j in range(img_height - 1, -1, -1):
        # Print real time render progress in-line
        progress = int(100 - 100 * j / img_height)
        if progress % 5 == 0 and progress != temp:
            temp = progress
            print('Progress: %d%%' % temp, end='\r', flush=True)

        for i in range(0, img_width):
            pixel_color = np.array([0, 0, 0], dtype=float)
            for _ in range(0, samples_per_pixel):
                u = (i + ru.get_random()) / (img_width - 1)
                v = (j + ru.get_random()) / (img_height - 1)
                pixel_color += ru.ray_color(camera.get_ray(u, v), world, max_depth)
            f.write(ru.color_to_str(pixel_color, samples_per_pixel))
    f.close()
    end = time.time()
    print("\nRender complete.\n")
    print("(normal) Time taken: " + str(end - start) + '\n')


def parallel_render():
    start = time.time()
    col_0 = np.array([[float(i) / (img_width-1) for _ in range(img_height - 1, -1, -1) for i in range(0, img_width)]]).T
    col_1 = np.array([[float(i) / (img_height-1) for i in range(img_height - 1, -1, -1) for _ in range(0, img_width)]]).T
    img = ru.parallel_ray_color(camera.lower_left_corner + col_0 * camera.horizontal + col_1 * camera.vertical - camera.origin)
    for pixel in img:
        f.write(ru.color_to_str(pixel, samples_per_pixel))
    f.close()
    end = time.time()
    print("(numpy) Time taken: " + str(end - start) + '\n')


def main():
    output_path = "../output/"
    output_name = "out"

    if len(sys.argv) == 1:
        output_path += output_name + ".ppm"
    elif len(sys.argv) == 2:
        output_name = sys.argv[1]
        output_path += output_name + ".ppm"
    else:
        print("Invalid input format.")
        raise

    global img_width, img_height, f, device, world, camera, samples_per_pixel, max_depth
    img_width = int(input("\nPlease enter the width of the output image:\n"))
    img_height = int(input("\nPlease enter the height of the output image:\n"))
    samples_per_pixel = int(input("\nPlease enter the number of samples per pixel:\n"))
    max_depth = int(input("\nPlease enter the max depth:\n"))

    if img_width > 1 and img_height > 1 and samples_per_pixel > 0 and max_depth > 0:
        print("\nFile: ", output_path, "\nWidth:  ", img_width, "px\nHeight: ", img_height, "px")
        print("#Samples / px: ", samples_per_pixel, "\nMax Depth: ", max_depth, "\n")
    else:
        print("Invalid output size.")
        raise

    """
        # world 1
        lookfrom = np.array([3.0, 3.0, 2.0])
        lookat = np.array([0.0, 0.0, -1.0])
        vup = np.array([0.0, 1.0, 0.0])
        vfov = 20.0
        aperature = 2.0
        focus_dist = ru.length(lookfrom - lookat)
    
        camera = Camera(img_width, img_height, lookfrom, lookat, vup, vfov, aperature, focus_dist)
    
        world = HittableList()
    
        mat_ground = Lambertian(np.array([0.8, 0.8, 0.0]))
        mat_center = Lambertian(np.array([0.1, 0.2, 0.5]))
        mat_left = Dielectric(1.5)
        mat_right = Metal(np.array([0.8, 0.6, 0.2]), 0.0)
    
        world.add(Sphere(np.array([0.0, -100.5, -1.0]), 100, mat_ground))
        world.add(Sphere(np.array([0.0, 0.0, -1.0]), 0.5, mat_center))
        world.add(Sphere(np.array([-1.0, 0.0, -1.0]), 0.5, mat_left))
        world.add(Sphere(np.array([-1.0, 0.0, -1.0]), -0.45, mat_left))
        world.add(Sphere(np.array([1.0, 0.0, -1.0]), 0.5, mat_right))
    
    """

    lookfrom = np.array([13.0, 2.0, 3.0])
    lookat = np.array([0.0, 0.0, 0.0])
    vup = np.array([0.0, 1.0, 0.0])
    vfov = 20.0
    aperature = 0.1
    focus_dist = 10.0  # ru.length(lookfrom - lookat)

    camera = Camera(img_width, img_height, lookfrom, lookat, vup, vfov, aperature, focus_dist)

    world = HittableList()

    mat_ground = Lambertian(np.array([0.5, 0.5, 0.5]))
    world.add(Sphere(np.array([0.0, -1000, 0.0]), 1000, mat_ground))

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
                world.add(Sphere(center, 0.2, sphere_material))

    mat1 = Dielectric(1.5)
    world.add(Sphere(np.array([0.0, 1.0, 0.0]), 1.0, mat1))

    mat2 = Lambertian(np.array([0.4, 0.2, 0.1]))
    world.add(Sphere(np.array([-4.0, 1.0, 0.0]), 1.0, mat2))

    mat3 = Metal(np.array([0.7, 0.6, 0.5]), 0.0)
    world.add(Sphere(np.array([4.0, 1.0, 0.0]), 1.0, mat3))

    # BVH implementation
    world.add(BVHNode(world.objects, 0, len(world.objects), 0, 1))

    f = open(output_path, "w")
    f.write("P3\n")
    f.write("# " + output_name + ".ppm\n")
    f.write("# Ray Tracer created by Zigeng Zhu (zigeng2@illinois.edu)\n")
    f.write(str(img_width) + " " + str(img_height) + "\n255\n")
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    torch.cuda.empty_cache()
    linear_render()


if __name__ == "__main__":
    main()
