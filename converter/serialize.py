#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""serialize.py

TODO.
"""

import sys
from pathlib import Path

import ffmpeg
import numpy as np

__author__ = "Vincent Lin"


def mp4_to_rgb(mp4_path: Path) -> np.ndarray:
    return np.array(0)


def compress_rgb(pixels: np.ndarray) -> np.ndarray:
    return np.array(0)


def write_bytes(compressed_pixels: np.ndarray) -> None:
    pass


def main() -> None:
    try:
        input_path = Path(sys.argv[1])
    except IndexError:
        sys.stderr.write(f"{sys.argv[0]}: Expected a file name.\n")
        sys.exit(22)

    rgb_pixels = mp4_to_rgb(input_path)
    compressed_pixels = compress_rgb(rgb_pixels)
    write_bytes(compressed_pixels)


if __name__ == "__main__":
    main()
