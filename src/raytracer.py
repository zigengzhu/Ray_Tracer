import numpy as np
import torch
import sys

def render_simple_img():
    for j in range(img_height-1, -1, -1):
        for i in range(0, img_width):
            r = float(i) / (img_width - 1)
            g = float(j) / (img_height - 1)
            b = 0.25

            ir = int(255.999 * r)
            ig = int(255.999 * g)
            ib = int(255.999 * b)

            f.write(str(ir) + ' ' + str(ig) + ' ' + str(ib) + '\n')

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

    global img_width, img_height, f
    img_width = int(input("Please enter the width of the output image:\n"))
    img_height = int(input("Please enter the height of the output image:\n"))

    if img_width > 0 and img_height > 0:
        print("\nFile: ", output_path, "\nWidth:  ", img_width, "px\nHeight: ", img_height, "px\n")
    else:
        print("Invalid output size.")
        raise

    f = open(output_path, "w")
    f.write("P3\n")
    f.write("# " + output_name + ".ppm\n")
    f.write("# Ray Tracer created by Zigeng Zhu (zigeng2@illinois.edu)\n")
    f.write(str(img_width) + " " + str(img_height) + "\n255\n")
    render_simple_img()
    print("File created.")
    f.close()

if __name__ == "__main__":
    main()
