#!/usr/bin/env python3
"""Build deterministic, pattern-only controls from a carpet artwork."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

from PIL import Image

from prepare_design_crop import BOXES


def _palette_and_labels(image: Image.Image, colours: int = 8):
    quantized = image.quantize(colors=colours, method=Image.Quantize.MEDIANCUT)
    palette = quantized.getpalette()
    pixels = (
        quantized.get_flattened_data()
        if hasattr(quantized, "get_flattened_data")
        else quantized.getdata()
    )
    counts = Counter(pixels)
    used = [index for index, _ in counts.most_common()]
    used_palette = {
        index: tuple(palette[index * 3 : index * 3 + 3])
        for index in used
    }
    return quantized, used_palette, counts


def _edge_map(labels: Image.Image) -> Image.Image:
    width, height = labels.size
    source = labels.load()
    edges = Image.new("L", labels.size, 0)
    target = edges.load()
    for y in range(height):
        for x in range(width):
            value = source[x, y]
            different = (
                (x > 0 and source[x - 1, y] != value)
                or (x + 1 < width and source[x + 1, y] != value)
                or (y > 0 and source[x, y - 1] != value)
                or (y + 1 < height and source[x, y + 1] != value)
            )
            target[x, y] = 255 if different else 0
    return edges


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("out_dir", type=Path)
    args = parser.parse_args()

    with Image.open(args.source) as loaded:
        image = loaded.convert("RGB")

    args.out_dir.mkdir(parents=True, exist_ok=True)
    width, height = image.size
    corner = "lower_left"
    left, top, right, bottom = BOXES[corner]
    crop_box = (
        round(width * left),
        round(height * top),
        round(width * right),
        round(height * bottom),
    )
    detail_crop = image.crop(crop_box)
    quantized, palette, counts = _palette_and_labels(image)

    region_map = quantized.convert("P")
    edge_map = _edge_map(quantized)
    detail_quantized, _, _ = _palette_and_labels(detail_crop)
    detail_edges = _edge_map(detail_quantized)

    detail_crop.save(args.out_dir / "design_detail_crop.png", format="PNG")
    region_map.save(args.out_dir / "design_region_map.png", format="PNG")
    region_map.save(args.out_dir / "design_region_mask.png", format="PNG")
    edge_map.save(args.out_dir / "design_edge_map.png", format="PNG")
    detail_edges.save(args.out_dir / "design_detail_edge_map.png", format="PNG")

    record = {
        "source": str(args.source.resolve()),
        "source_sha256": _sha256(args.source),
        "source_size": [width, height],
            "detail_corner": corner,
        "detail_crop_box": list(crop_box),
        "palette": [
            {"quantized_index": index, "rgb": list(rgb), "pixel_count": counts[index]}
            for index, rgb in palette.items()
        ],
        "controls": {
            "design_detail_crop": "design_detail_crop.png",
            "design_region_map": "design_region_map.png",
            "design_region_mask": "design_region_mask.png",
            "design_edge_map": "design_edge_map.png",
            "design_detail_edge_map": "design_detail_edge_map.png",
        },
        "topology_mode": "strict",
        "material_authority": "none",
    }
    (args.out_dir / "design_lock.json").write_text(
        json.dumps(record, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(record, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
