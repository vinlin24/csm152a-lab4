#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""visualizer.py

Script for visualizing the difference in coloring between a 160x120px
24-bit RGB frame and its 8-bit RGB version.

This script can read from a binary file containing the raw pixel bytes
of a certain video frame:

Usage: `./visualizer.py frame_data`

If no command line argument is given, the script will read from stdin.
This can be useful if you're dumping with an external command, like xxd.

Usage: `cat frame_data | ./visualizer.py`
"""

import sys
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np

__author__ = "Vincent Lin"

FRAME_NCOLS = 160
FRAME_NROWS = 120
PIXEL_NBYTES = 3

FRAME_NBYTES = FRAME_NCOLS * FRAME_NROWS * PIXEL_NBYTES


def to_8bit(r: int, g: int, b: int) -> int:
    r_slice = (r & 0b11100000) >> 0
    g_slice = (g & 0b11100000) >> 3
    b_slice = (b & 0b11000000) >> 6
    return r_slice | g_slice | b_slice


def from_8bit(byte: int) -> Tuple[int, int, int]:
    r = (byte & 0b11100000) << 0
    g = (byte & 0b00011100) << 3
    b = (byte & 0b00000011) << 6
    return (r, g, b)


def cast_rgb(rgb: np.ndarray) -> Tuple[int, int, int]:
    r, g, b = rgb
    return from_8bit(to_8bit(r, g, b))  # Round trip.


def main() -> None:
    argc = len(sys.argv)
    if argc >= 2:
        input_file = sys.argv[1]
        with open(input_file, "rb") as source:
            input_data = source.read()
    else:
        input_data = sys.stdin.buffer.read(FRAME_NBYTES)

    input_nbytes = len(input_data)
    if input_nbytes != FRAME_NBYTES:
        sys.stderr.write(
            f"{sys.argv[0]}: Expected {FRAME_NBYTES} bytes of data, "
            f"got {input_nbytes} instead.\n"
        )
        sys.exit(22)

    # Convert bytes to ints.
    byte_values = list(input_data)

    pixels_original = np.reshape(byte_values,
                                 (FRAME_NROWS, FRAME_NCOLS, PIXEL_NBYTES))
    plt.figure()
    plt.title("Compressed Frame")
    plt.imshow(pixels_original)

    pixels_8bit = np.apply_along_axis(cast_rgb, 2, pixels_original)
    plt.figure()
    plt.title("Frame Using 8-bit Coloring")
    plt.imshow(pixels_8bit)

    plt.show()


if __name__ == "__main__":
    main()
