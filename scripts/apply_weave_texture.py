#!/usr/bin/env python3
"""Apply real multi-scale weave relief to an accepted overview without changing its design."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter, ImageOps


def mirrored_texture(path: Path, tile_width: int, width: int, height: int) -> np.ndarray:
    with Image.open(path) as opened:
        gray = ImageOps.grayscale(ImageOps.exif_transpose(opened))
        tile_height = max(32, round(gray.height * tile_width / gray.width))
        tile = np.asarray(gray.resize((tile_width, tile_height), Image.Resampling.LANCZOS), dtype=np.float32)
    block = np.block([[tile, np.fliplr(tile)], [np.flipud(tile), np.flipud(np.fliplr(tile))]])
    copies_y = (height + block.shape[0] - 1) // block.shape[0]
    copies_x = (width + block.shape[1] - 1) // block.shape[1]
    return np.tile(block, (copies_y, copies_x))[:height, :width]


def relief(texture: np.ndarray, blur_radius: float) -> np.ndarray:
    base = Image.fromarray(np.clip(texture, 0, 255).astype(np.uint8), mode="L")
    blurred = np.asarray(base.filter(ImageFilter.GaussianBlur(blur_radius)), dtype=np.float32)
    high = texture - blurred
    scale = max(float(np.percentile(np.abs(high), 90)), 1.0)
    return np.clip(high / scale, -1.8, 1.8)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--product-texture", type=Path, required=True)
    parser.add_argument("--macro-texture", type=Path, required=True)
    parser.add_argument("--product-tile", type=int, default=240)
    parser.add_argument("--macro-tile", type=int, default=150)
    parser.add_argument("--product-strength", type=float, default=0.13)
    parser.add_argument("--macro-strength", type=float, default=0.045)
    args = parser.parse_args()

    with Image.open(args.input) as opened:
        source = ImageOps.exif_transpose(opened).convert("RGB")
    rgb = np.asarray(source, dtype=np.float32) / 255.0
    height, width = rgb.shape[:2]

    product = mirrored_texture(args.product_texture, args.product_tile, width, height)
    macro = mirrored_texture(args.macro_texture, args.macro_tile, width, height)
    product_relief = relief(product, max(2.0, args.product_tile / 28.0))
    macro_relief = relief(macro, max(1.2, args.macro_tile / 35.0))

    luminance = rgb.mean(axis=2)
    chroma = rgb.max(axis=2) - rgb.min(axis=2)
    # Keep the white studio sweep and its soft contact shadow clean. Cream yarns
    # are substantially darker/more chromatic than the background, so this mask
    # still includes the complete rug while excluding near-white pixels.
    rug_mask = np.clip((0.94 - luminance) / 0.04 + chroma * 1.25, 0.0, 1.0)
    modulation = np.exp(
        rug_mask * (args.product_strength * product_relief + args.macro_strength * macro_relief)
    )
    result = np.clip(rgb * modulation[..., None], 0.0, 1.0)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(np.round(result * 255).astype(np.uint8), mode="RGB").save(
        args.output, compress_level=3
    )
    print(
        {
            "input": str(args.input.resolve()),
            "output": str(args.output.resolve()),
            "size": [width, height],
            "product_tile": args.product_tile,
            "macro_tile": args.macro_tile,
        }
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
