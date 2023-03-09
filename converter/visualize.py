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

__author__ = "Vincent Lin"

FRAMES_PER_SEC = 16


def secs_to_frame_num(num_secs: int) -> int:
    return 0  # TODO.


def secs_to_MMSS(num_secs: float) -> str:
    mins, secs = divmod(num_secs, 60)
    return f"{int(mins):02}:{secs:05.2f}"


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
    time_pos = secs_to_MMSS(frame_pos_sec)

    cv2.imshow(f"Frame {frame_num} ({time_pos})", frame)
    cv2.waitKey(0)
    capture.release()
    cv2.destroyAllWindows()


def show_rgb_frame(input_file: Path, frame_num: int) -> None:
    pass


def show_bin_frame(input_file: Path, frame_num: int) -> None:
    pass


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
                    choices=("mp4", "rgb", "bin"), default="bin",
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
    file_format: Literal["mp4", "rgb", "bin"] = namespace.file_format
    frame_num: Optional[int] = namespace.frame_num
    num_secs: Optional[int] = namespace.num_secs

    if num_secs is not None:
        frame_num = secs_to_frame_num(num_secs)

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
