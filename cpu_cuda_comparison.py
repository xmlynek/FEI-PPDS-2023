"""This module compares the performance of CPU and GPU implementations
of image conversion to grayscale. The conversion using GPU is done through
Numba CUDA parallel computing.
"""

__author__ = "Filip Mlýnek, Tomáš Vavro, ChatGPT"
__email__ = "xmlynek@stuba.sk, xvavro@stuba.sk"
__license__ = "MIT"

from numba import cuda
import matplotlib.pyplot as plt
import numpy as np
import os
import time

INPUT_DIR_NAME = "input_images"
CPU_OUTPUT_DIR_NAME = "cpu_output_images"
GPU_OUTPUT_DIR_NAME = "gpu_output_images"


@cuda.jit
def kernel(img, gray_img):
    """Converts a color image to grayscale using Numba CUDA parallel computing.

    Args:
            img: The input of the original image.
            gray_img: The output grayscale image.
    """
    x, y = cuda.grid(2)

    if x < gray_img.shape[0] and y < gray_img.shape[1]:
        gray_value = 0.2989 * img[x, y, 0] + 0.5870 * img[x, y, 1] + 0.1140 * \
                     img[x, y, 2]

        gray_img[x, y, 0] = gray_value
        gray_img[x, y, 1] = gray_value
        gray_img[x, y, 2] = gray_value


def gpu():
    """Converts every image in the directory to grayscale using Numba CUDA
    parallel computing and measures elapsed time per conversion.
    """
    avg_time = []
    for filename in os.listdir(INPUT_DIR_NAME):
        start = time.time()
        img = plt.imread(f"./{INPUT_DIR_NAME}/{filename}")

        threads_per_block = (32, 32)
        blocks_per_grid = (int(np.ceil(img.shape[0] / threads_per_block[0])),
                           int(np.ceil(img.shape[1] / threads_per_block[1])))

        gray_img = np.empty_like(img)

        d_img = cuda.to_device(img)
        d_gray_img = cuda.device_array_like(gray_img)

        kernel[threads_per_block, blocks_per_grid](d_img, d_gray_img)

        d_gray_img.copy_to_host(gray_img)
        plt.imsave(f"./{GPU_OUTPUT_DIR_NAME}/{filename}", gray_img,
                   cmap='gray')

        stop = time.time() - start
        print(f"GPU Time: {stop} sec")
        avg_time.append(stop)
    print(f"Average time of conversion using GPU: "
          f"{sum(avg_time) / len(avg_time)}")


def cpu():
    """Converts every image in the directory to grayscale using CPU
    and measures elapsed time per conversion.
    """
    avg_time = []
    for filename in os.listdir(INPUT_DIR_NAME):
        start = time.time()
        img = plt.imread(f"./{INPUT_DIR_NAME}/{filename}")
        gray_img = 0.2989 * img[:, :, 0] + 0.5870 * img[:, :, 1] + 0.1140 * img[
                                                                            :,
                                                                            :,
                                                                            2]
        plt.imsave(f"./{CPU_OUTPUT_DIR_NAME}/{filename}", gray_img,
                   cmap='gray')
        stop = time.time() - start
        print(f"CPU Time: {stop} sec")
        avg_time.append(stop)
    print(f"Average time of conversion using CPU: "
          f"{sum(avg_time) / len(avg_time)}")


if __name__ == '__main__':
    """Main function to compare the performance of CPU and GPU implementations
    of image conversion to grayscale.
    """
    start_time = time.time()
    cpu()
    print("--- CPU execution %s seconds ---" % (time.time() - start_time))

    start_time = time.time()
    gpu()
    print("--- GPU execution %s seconds ---" % (time.time() - start_time))
