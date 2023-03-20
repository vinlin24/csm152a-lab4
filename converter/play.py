"""play.py

Play a bin file.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from constants import FRAME_NCOLS, FRAME_NROWS
from visualize import to_24bit


def main() -> None:
    try:
        bin_path = Path(sys.argv[1])
    except IndexError:
        sys.stderr.write(f"Expected a file.\n")
        sys.exit(22)

    bin_bytes = np.fromfile(bin_path, dtype=np.uint8)

    num_frames, remainder = divmod(bin_bytes.size, FRAME_NROWS * FRAME_NCOLS)
    assert remainder == 0

    frames = np.reshape(bin_bytes, (num_frames, FRAME_NROWS, FRAME_NCOLS))

    for frame_num, frame in enumerate(frames):
        plt.figure()
        plt.title(f"{bin_path}: Frame {frame_num}")
        plt.imshow(to_24bit(frame))

    plt.show()


if __name__ == "__main__":
    main()
