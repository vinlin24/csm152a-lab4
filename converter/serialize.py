#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""serialize.py

TODO.
"""

import subprocess
import sys
from argparse import ArgumentParser
from pathlib import Path

import numpy as np

__author__ = "Vincent Lin"

FFMPEG_OPTIONS = {
    "vf": "scale=160:120",
    "r": 16,
    "pix_fmt": "rgb24",
}

FRAME_NCOLS = 160
FRAME_NROWS = 120
PIXEL_NBYTES = 3

FRAME_NBYTES = FRAME_NCOLS * FRAME_NROWS * PIXEL_NBYTES

parser = ArgumentParser(prog=Path(sys.argv[0]).name,
                        description="TODO.")

parser.add_argument("mp4_path", metavar="MP4_FILE", type=Path)
parser.add_argument("bin_path", metavar="BIN_FILE", type=Path)


def run(script: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(script, shell=True, capture_output=True, check=True)


def mp4_to_rgb(mp4_path: Path) -> Path:
    mp4_name = mp4_path.stem
    output_path = mp4_path.parent / Path(f"{mp4_name}.rgb")

    # Remove without warning lol.
    output_path.unlink(missing_ok=True)

    options = " ".join(f"-{flag} {arg}"
                       for flag, arg in FFMPEG_OPTIONS.items())
    command = f"ffmpeg -i {mp4_path} {options} {output_path}"
    print(command)
    run(command)

    return output_path


def load_rgb_as_frames(rgb_path: Path) -> np.ndarray:
    rgb_bytes = np.fromfile(rgb_path, dtype=np.uint8)

    assert rgb_bytes.size % FRAME_NBYTES == 0, \
        f"{rgb_path} has {rgb_bytes.size} bytes, which is not a multiple of " \
        f"{FRAME_NBYTES}: ({FRAME_NCOLS=})*({FRAME_NROWS=})*({PIXEL_NBYTES=})."

    num_frames: int = rgb_bytes.size // FRAME_NBYTES
    frames = np.reshape(rgb_bytes,
                        (num_frames, FRAME_NROWS, FRAME_NCOLS, PIXEL_NBYTES))
    print(f"Loaded {num_frames} frames from {rgb_path}.")
    return frames


def compress_rgb_frames(frames: np.ndarray) -> np.ndarray:
    # Vectorized operations go brr.
    r = frames[..., 0]
    g = frames[..., 1]
    b = frames[..., 2]
    # Compress 24-bit RGB to 8-bit RGB by taking the most significant
    # bits of each channel.
    r_slice = (r & 0b11100000) >> 0
    g_slice = (g & 0b11100000) >> 3
    b_slice = (b & 0b11000000) >> 6
    # Concatenate the components.  This also flattens the frames array
    # from 4D to 3D by converting the pixel axis into uint8 scalars.
    compressed_frames = r_slice | g_slice | b_slice
    print("Compressed 24-bit RGB channels into 8-bit scalars.")
    return compressed_frames


def write_bytes(compressed_pixels: np.ndarray, bin_path: Path) -> None:
    linear_bytes = compressed_pixels.flatten()
    linear_bytes.tofile(bin_path)
    num_kilobytes = linear_bytes.size / 1000
    print(f"Wrote {num_kilobytes:.2f}K to {bin_path}.")


def main() -> None:
    namespace = parser.parse_args()
    mp4_path: Path = namespace.mp4_path
    bin_path: Path = namespace.bin_path

    rgb_path = mp4_to_rgb(mp4_path)
    rgb_frames = load_rgb_as_frames(rgb_path)
    compressed_frames = compress_rgb_frames(rgb_frames)
    write_bytes(compressed_frames, bin_path)


if __name__ == "__main__":
    main()
