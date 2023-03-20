#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Load a video file in .bin format and format how it would be hard-coded
in a Verilog source file.
"""

import io
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import List, Optional

import numpy as np
from constants import FRAME_NCOLS, FRAME_NROWS, PIXEL_NBYTES

ARRAY_NAME = "frames"

parser = ArgumentParser(prog=Path(sys.argv[0]).name, description=__doc__)

parser.add_argument("bin_path", metavar="BIN_PATH", type=Path,
                    help="path of binary file to transpile")
parser.add_argument("txt_path", metavar="TXT_PATH", type=Path, nargs="?",
                    help="path of output file (default stdout)")


def frame_to_assignments(frame: np.ndarray, frame_num: int) -> str:
    template = f"{ARRAY_NAME}[{frame_num}]"
    template += "[{row_index}][{col_index}] = 8'h{hex_pair};"
    assignments = io.StringIO()
    for row_index, row in enumerate(frame):
        for col_index, byte in enumerate(row):
            hex_pair = hex(byte).removeprefix("0x").zfill(2)
            assignment = template.format(
                row_index=row_index, col_index=col_index, hex_pair=hex_pair)
            assignments.write(f"{assignment}\n")
    return assignments.getvalue()


def main() -> None:
    namespace = parser.parse_args()
    bin_path: Path = namespace.bin_path
    txt_path: Optional[Path] = namespace.txt_path

    bin_bytes = np.fromfile(bin_path, dtype=np.uint8)

    num_frames, remainder = divmod(bin_bytes.size, FRAME_NROWS * FRAME_NCOLS)
    assert remainder == 0, \
        f"{bin_path} has {bin_bytes.size} bytes, which is not a multiple of " \
        f"{FRAME_NROWS=}*{FRAME_NCOLS=}={FRAME_NROWS*FRAME_NCOLS}."

    sys.stderr.write(
        f"Loaded {num_frames} 160x120px frames from {bin_path}.\n")

    frames = np.reshape(bin_bytes, (num_frames, FRAME_NROWS, FRAME_NCOLS))

    result = io.StringIO()
    for frame_num, frame in enumerate(frames):
        assignments = frame_to_assignments(frame, frame_num)
        result.write(assignments)

    if txt_path is None:
        dest = sys.stdout
    else:
        dest = txt_path.open("wt", encoding="utf-8")

    with dest:
        dest.write(result.getvalue())


if __name__ == "__main__":
    main()
