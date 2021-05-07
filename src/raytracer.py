import sys
from scene import Scene

"""
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
"""


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

    img_width = int(input("\nPlease enter the width of the output image:\n"))
    img_height = int(input("\nPlease enter the height of the output image:\n"))
    samples_per_pixel = int(input("\nPlease enter the number of samples per pixel:\n"))
    max_depth = int(input("\nPlease enter the max depth:\n"))

    s = Scene(output_path, img_width, img_height, samples_per_pixel, max_depth, setting="cornell_box")
    s.render()

    # device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    # torch.cuda.empty_cache()


if __name__ == "__main__":
    main()
