#!/usr/bin/env bash

if [ $# -lt 2 ]; then
    echo >&2 "Usage: $0 RGB_FILE FRAME_NUM"
    echo >&2 "Frame numbers start counting from 0."
    exit 22
fi

input_file="$1"
frame_num=$2

FRAME_NCOLS=160
FRAME_NROWS=120
PIXEL_NBYTES=3

FRAME_NBYTES=$((FRAME_NCOLS * FRAME_NROWS * PIXEL_NBYTES))
offset=$((frame_num * FRAME_NBYTES))

dd if="$input_file" skip=$offset count=$FRAME_NBYTES bs=1 2>/dev/null
