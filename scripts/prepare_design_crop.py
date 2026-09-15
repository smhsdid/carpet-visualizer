#!/usr/bin/env python3
"""Create a deterministic pattern reference crop from an upright rug design."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


BOXES = {
    "upper_left": (0.00, 0.00, 0.58, 0.42),
    "upper_right": (0.42, 0.00, 1.00, 0.42),
    "lower_left": (0.00, 0.58, 0.58, 1.00),
    "lower_right": (0.42, 0.58, 1.00, 1.00),
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("out", type=Path)
    parser.add_argument("--corner", choices=BOXES, default="lower_left")
    args = parser.parse_args()

    with Image.open(args.source) as source:
        image = source.convert("RGB")
        width, height = image.size
        left, top, right, bottom = BOXES[args.corner]
        box = (
            round(width * left),
            round(height * top),
            round(width * right),
            round(height * bottom),
        )
        args.out.parent.mkdir(parents=True, exist_ok=True)
        image.crop(box).save(args.out, format="PNG")


if __name__ == "__main__":
    main()
