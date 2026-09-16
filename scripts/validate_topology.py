#!/usr/bin/env python3
"""Validate an aligned structure proof against the current design.

The proof must be in source coordinates and must exist before material and
camera rendering. This script intentionally does not bless a perspective
product photograph.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

from PIL import Image


GRID = 128


def _source_palette(image: Image.Image, colours: int = 8):
    quantized = image.quantize(colors=colours, method=Image.Quantize.MEDIANCUT)
    palette = quantized.getpalette()
    pixels = (
        quantized.get_flattened_data()
        if hasattr(quantized, "get_flattened_data")
        else quantized.getdata()
    )
    counts = Counter(pixels)
    used = [index for index, _ in counts.most_common()]
    rgb = {
        index: tuple(palette[index * 3 : index * 3 + 3])
        for index in used
    }
    return quantized, rgb


def _nearest_label(pixel: tuple[int, int, int], palette: dict[int, tuple[int, int, int]]) -> int:
    return min(
        palette,
        key=lambda index: sum((pixel[i] - palette[index][i]) ** 2 for i in range(3)),
    )


def _labels_for_output(image: Image.Image, palette: dict[int, tuple[int, int, int]]) -> Image.Image:
    result = Image.new("L", image.size)
    source = image.load()
    target = result.load()
    for y in range(image.height):
        for x in range(image.width):
            target[x, y] = _nearest_label(source[x, y], palette)
    return result


def _resize_labels(labels: Image.Image) -> Image.Image:
    return labels.resize((GRID, GRID), Image.Resampling.NEAREST)


def _edges(labels: Image.Image) -> set[tuple[int, int]]:
    source = labels.load()
    result: set[tuple[int, int]] = set()
    for y in range(GRID):
        for x in range(GRID):
            value = source[x, y]
            if (x + 1 < GRID and source[x + 1, y] != value) or (
                y + 1 < GRID and source[x, y + 1] != value
            ):
                result.add((x, y))
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("proof", type=Path)
    parser.add_argument(
        "--aligned",
        action="store_true",
        required=True,
        help="affirm that proof is a source-coordinate structure proof, not a perspective photo",
    )
    parser.add_argument("--max-region-error", type=float, default=0.02)
    parser.add_argument("--min-boundary-f1", type=float, default=0.95)
    args = parser.parse_args()

    with Image.open(args.source) as loaded_source:
        source = loaded_source.convert("RGB")
    with Image.open(args.proof) as loaded_proof:
        proof = loaded_proof.convert("RGB")

    _, palette = _source_palette(source)
    # Quantizers may assign a source pixel to a palette entry that is not its
    # nearest RGB entry. Label both sides through the same nearest-palette
    # operation so an identical source-coordinate proof is an exact pass.
    source_labels = _labels_for_output(source, palette)
    proof_labels = _labels_for_output(proof, palette)
    source_grid = _resize_labels(source_labels)
    proof_grid = _resize_labels(proof_labels)

    source_pixels = source_grid.load()
    proof_pixels = proof_grid.load()
    mismatches = sum(
        source_pixels[x, y] != proof_pixels[x, y]
        for y in range(GRID)
        for x in range(GRID)
    )
    region_error = mismatches / (GRID * GRID)

    source_edges = _edges(source_grid)
    proof_edges = _edges(proof_grid)
    true_positive = len(source_edges & proof_edges)
    precision = true_positive / len(proof_edges) if proof_edges else 0.0
    recall = true_positive / len(source_edges) if source_edges else 0.0
    boundary_f1 = (
        2 * precision * recall / (precision + recall)
        if precision + recall
        else 0.0
    )
    passed = (
        region_error <= args.max_region_error
        and boundary_f1 >= args.min_boundary_f1
    )
    result = {
        "status": "pass" if passed else "fail",
        "comparison": "aligned_source_coordinate_proof_only",
        "source": str(args.source.resolve()),
        "proof": str(args.proof.resolve()),
        "grid": GRID,
        "region_error": round(region_error, 6),
        "boundary_f1": round(boundary_f1, 6),
        "thresholds": {
            "max_region_error": args.max_region_error,
            "min_boundary_f1": args.min_boundary_f1,
        },
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
