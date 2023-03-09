#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TODO.
"""

import sys
from argparse import ArgumentParser, ArgumentTypeError
from pathlib import Path
from typing import Literal, Optional

import cv2
import matplotlib.pyplot as plt
import numpy as np

__author__ = "Vincent Lin"

FRAMES_PER_SEC = 16

FRAME_NCOLS = 160
FRAME_NROWS = 120
PIXEL_NBYTES = 3

NUM_PIXELS = FRAME_NCOLS * FRAME_NROWS
FRAME_NBYTES = NUM_PIXELS * PIXEL_NBYTES


def secs_to_frame_num(num_secs: int) -> int:
    return 0  # TODO.


def secs_to_MMSS(num_secs: float) -> str:
    mins, secs = divmod(num_secs, 60)
    return f"{int(mins):02}:{secs:05.2f}"


def show(frame: np.ndarray, frame_num: int, frame_sec: float, origin_path: Path
         ) -> None:
    time_pos = secs_to_MMSS(frame_sec)
    plt.title(f"{origin_path}: Frame {frame_num} ({time_pos})")
    plt.imshow(frame)
    plt.show()


def to_24bit(compressed_frame: np.ndarray) -> np.ndarray:
    r = (compressed_frame & 0b11100000) << 0
    g = (compressed_frame & 0b00011100) << 3
    b = (compressed_frame & 0b00000011) << 6
    frame = np.expand_dims(compressed_frame, axis=-1)
    frame = np.repeat(frame, 3, axis=-1)
    frame[..., 0] = r
    frame[..., 1] = g
    frame[..., 2] = b
    return frame


def show_mp4_frame(mp4_path: Path, frame_num: int) -> None:
    capture = cv2.VideoCapture(str(mp4_path))

    frame = None
    for _ in range(frame_num + 1):
        _, frame = capture.read()
    if frame is None:
        raise ValueError(
            f"{frame_num} is an invalid frame number for {mp4_path}.")

    capture.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
    frame_pos_ms = capture.get(cv2.CAP_PROP_POS_MSEC)
    frame_pos_sec = frame_pos_ms / 1000
    show(frame, frame_num, frame_pos_sec, mp4_path)


def show_rgb_frame(rgb_path: Path, frame_num: int) -> None:
    offset = frame_num * FRAME_NBYTES

    rgb_bytes = np.fromfile(rgb_path, dtype=np.uint8,
                            count=FRAME_NBYTES, offset=offset)

    assert rgb_bytes.size == FRAME_NBYTES, \
        f"{rgb_path} has {rgb_bytes.size} bytes, expected {FRAME_NBYTES}."

    frame = np.reshape(rgb_bytes, (FRAME_NROWS, FRAME_NCOLS, PIXEL_NBYTES))

    num_secs = frame_num / FRAMES_PER_SEC
    show(frame, frame_num, num_secs, rgb_path)


def show_bin_frame(bin_path: Path, frame_num: int) -> None:
    offset = frame_num * NUM_PIXELS

    bin_bytes = np.fromfile(bin_path, dtype=np.uint8,
                            count=NUM_PIXELS, offset=offset)

    assert bin_bytes.size == NUM_PIXELS, \
        f"{bin_path} has {bin_bytes.size} bytes, expected {NUM_PIXELS}."

    compressed_frame = np.reshape(bin_bytes, (FRAME_NROWS, FRAME_NCOLS))
    frame = to_24bit(compressed_frame)

    num_secs = frame_num / FRAMES_PER_SEC
    show(frame, frame_num, num_secs, bin_path)


parser = ArgumentParser(prog=Path(sys.argv[0]).name, description=__doc__)


def nonnegative_int(value: str) -> int:
    if value.startswith("0x"):
        as_int = int(value, 16)
    elif value.startswith("0o"):
        as_int = int(value, 8)
    elif value.startswith("0b"):
        as_int = int(value, 2)
    else:
        as_int = int(value)

    if as_int < 0:
        raise ArgumentTypeError(f"{value} is an invalid non-negative int.")
    return as_int


parser.add_argument("input_path", metavar="FILE", type=Path,
                    help="TODO.")
parser.add_argument("-t", "--type", metavar="FILE_FMT", dest="file_format",
                    choices=("mp4", "rgb", "bin"),
                    help="TODO.")

offset_group = parser.add_mutually_exclusive_group(required=True)

offset_group.add_argument("-f", "--frame", metavar="FRAME", dest="frame_num",
                          type=nonnegative_int,
                          help="TODO.")
offset_group.add_argument("-s", "--seconds", metavar="SECS", dest="num_secs",
                          type=nonnegative_int,
                          help="TODO.")


def main() -> None:
    namespace = parser.parse_args()
    input_path: Path = namespace.input_path
    file_format: Optional[str] = namespace.file_format
    frame_num: Optional[int] = namespace.frame_num
    num_secs: Optional[int] = namespace.num_secs

    if num_secs is not None:
        frame_num = secs_to_frame_num(num_secs)

    # Infer the file type from the extension.
    if file_format is None:
        extension = input_path.suffix.removeprefix(".")
        file_format = extension

    if file_format == "mp4":
        func = show_mp4_frame
    elif file_format == "rgb":
        func = show_rgb_frame
    elif file_format == "bin":
        func = show_bin_frame
    else:
        raise ValueError(f"Invalid file format: {file_format!r}.")

    func(input_path, frame_num)  # type: ignore


if __name__ == "__main__":
    main()
