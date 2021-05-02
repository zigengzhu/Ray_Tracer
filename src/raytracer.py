import time

import numpy as np
import torch
import sys
import rtxUtil as ru
from hittable import HittableList
from sphere import Sphere
from camera import Camera
from material import Lambertian, Metal, Dielectric


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
    camera = Camera(img_width, img_height)

    if img_width > 1 and img_height > 1 and samples_per_pixel > 0 and max_depth > 0:
        print("\nFile: ", output_path, "\nWidth:  ", img_width, "px\nHeight: ", img_height, "px")
        print("Samples Per Pixel: ", samples_per_pixel, "\nMax Depth: ", max_depth, "\n")
    else:
        print("Invalid output size.")
        raise

    mat_ground = Lambertian(np.array([0.8, 0.8, 0.0]))
    mat_center = Dielectric(1.5)
    mat_left = Metal(np.array([0.8, 0.8, 0.8]), 0.3)
    mat_right = Metal(np.array([0.8, 0.6, 0.2]), 1.0)

    world = HittableList()
    world.add(Sphere(np.array([0.0, 0.0, -1.0]), 0.5, mat_center))
    world.add(Sphere(np.array([0.0, -100.5, -1.0]), 100, mat_ground))
    world.add(Sphere(np.array([-1.0, 0.0, -1.0]), 0.5, mat_left))
    world.add(Sphere(np.array([-1.0, 0.0, -1.0]), -0.4, mat_left))
    world.add(Sphere(np.array([1.0, 0.0, -1.0]), 0.5, mat_right))

    f = open(output_path, "w")
    f.write("P3\n")
    f.write("# " + output_name + ".ppm\n")
    f.write("# Ray Tracer created by Zigeng Zhu (zigeng2@illinois.edu)\n")
    f.write(str(img_width) + " " + str(img_height) + "\n255\n")

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    torch.cuda.empty_cache()

    linear_render()
    #parallel_render()


if __name__ == "__main__":
    main()
