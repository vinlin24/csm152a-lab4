#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""serialize.py

TODO.
"""

import subprocess
import sys
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

    rgb_path = mp4_to_rgb(input_path)
    rgb_frames = load_rgb_as_frames(rgb_path)


if __name__ == "__main__":
    main()
