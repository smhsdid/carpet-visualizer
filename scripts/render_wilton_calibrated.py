#!/usr/bin/env python3
"""Create diagnostic source-coordinate structure evidence for Wilton flatweave.

This helper is deliberately proof-only. Its synthetic yarn primitives are not
real-reference-grounded enough to be delivered as a material detail or product
overview. User-facing visuals must use the reference-grounded image route.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CALIBRATION = (
    ROOT / "assets" / "material-library" / "wilton-flatweave-01" / "paired-mappings.json"
)
DETAIL_BOX = (0.0, 0.58, 0.58, 1.0)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def clamp(value: float) -> int:
    return max(0, min(255, round(value)))


def mix(left: tuple[int, int, int], right: tuple[int, int, int], amount: float) -> tuple[int, int, int]:
    return tuple(clamp(left[i] * (1 - amount) + right[i] * amount) for i in range(3))


def darken(colour: tuple[int, int, int], amount: float) -> tuple[int, int, int]:
    return tuple(clamp(channel * amount) for channel in colour)


def sample_colour(colour_map: Image.Image, x: float, y: float) -> tuple[int, int, int]:
    point = (
        max(0, min(colour_map.width - 1, round(x))),
        max(0, min(colour_map.height - 1, round(y))),
    )
    pixel = colour_map.getpixel(point)
    return tuple(int(channel) for channel in pixel[:3])


def perspective_coefficients(
    input_points: list[tuple[float, float]], output_points: list[tuple[float, float]]
) -> tuple[float, ...]:
    matrix: list[list[float]] = []
    rhs: list[float] = []
    for (x, y), (u, v) in zip(input_points, output_points):
        matrix.extend(
            ([x, y, 1, 0, 0, 0, -u * x, -u * y], [0, 0, 0, x, y, 1, -v * x, -v * y])
        )
        rhs.extend((u, v))
    augmented = [matrix[index][:] + [rhs[index]] for index in range(8)]
    for column in range(8):
        pivot = max(range(column, 8), key=lambda row: abs(augmented[row][column]))
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        divisor = augmented[column][column]
        if abs(divisor) < 1e-12:
            raise ValueError("singular perspective transform")
        for offset in range(column, 9):
            augmented[column][offset] /= divisor
        for row in range(8):
            if row == column:
                continue
            factor = augmented[row][column]
            for offset in range(column, 9):
                augmented[row][offset] -= factor * augmented[column][offset]
    return tuple(augmented[index][8] for index in range(8))


def warp_plane(
    plane: Image.Image, canvas_size: tuple[int, int], destination: list[tuple[float, float]]
) -> tuple[Image.Image, Image.Image]:
    source = [(0, 0), (plane.width - 1, 0), (plane.width - 1, plane.height - 1), (0, plane.height - 1)]
    coefficients = perspective_coefficients(destination, source)
    warped = plane.transform(canvas_size, Image.Transform.PERSPECTIVE, coefficients, Image.Resampling.BICUBIC)
    mask = Image.new("L", plane.size, 255).transform(
        canvas_size, Image.Transform.PERSPECTIVE, coefficients, Image.Resampling.BICUBIC
    )
    return warped, mask


def draw_backdrop(size: tuple[int, int], seed: int) -> Image.Image:
    """A neutral dark textile ground matching the product-record family."""
    rng = random.Random(seed)
    image = Image.new("RGB", size, (34, 41, 50))
    draw = ImageDraw.Draw(image, "RGBA")
    for y in range(-4, size[1] + 4, 7):
        offset = rng.randint(-3, 3)
        for x in range(-6, size[0] + 6, 9):
            shade = rng.randint(12, 38)
            draw.arc((x + offset, y, x + 10 + offset, y + 7), 180, 360, fill=(86, 97, 109, shade), width=1)
    return image.filter(ImageFilter.GaussianBlur(0.25))


def draw_binding(
    image: Image.Image,
    colour_map: Image.Image,
    width: int,
    height: int,
    ratio: float,
    lock_ratio: float,
    sides: tuple[str, ...],
) -> None:
    draw = ImageDraw.Draw(image, "RGBA")
    thickness = max(10, round(min(width, height) * ratio))
    lock = max(2, round(thickness * lock_ratio))
    colours = {
        "left": sample_colour(colour_map, 3, height * 0.5),
        "right": sample_colour(colour_map, width - 4, height * 0.5),
        "top": sample_colour(colour_map, width * 0.5, 3),
        "bottom": sample_colour(colour_map, width * 0.5, height - 4),
    }
    positions = {
        "left": ((thickness // 2, 0, thickness // 2, height), (thickness + lock, 4, thickness + lock, height - 4)),
        "right": ((width - thickness // 2, 0, width - thickness // 2, height), (width - thickness - lock, 4, width - thickness - lock, height - 4)),
        "top": ((0, thickness // 2, width, thickness // 2), (4, thickness + lock, width - 4, thickness + lock)),
        "bottom": ((0, height - thickness // 2, width, height - thickness // 2), (4, height - thickness - lock, width - 4, height - thickness - lock)),
    }
    for side in sides:
        colour = colours[side]
        main, inner = positions[side]
        draw.line(main, fill=(*darken(colour, 0.55), 255), width=thickness + 4)
        draw.line(main, fill=(*mix(colour, (245, 238, 222), 0.18), 255), width=thickness)
        draw.line(inner, fill=(*darken(colour, 0.50), 230), width=lock)
        for strand in range(3, thickness - 2, 3):
            light = (*mix(colour, (255, 249, 231), 0.42 if strand % 2 else 0.18), 125)
            if side in {"left", "right"}:
                x = strand if side == "left" else width - strand
                draw.line((x, 0, x, height), fill=light, width=1)
            else:
                y = strand if side == "top" else height - strand
                draw.line((0, y, width, y), fill=light, width=1)


def synthesize_surface(
    source: Image.Image,
    size: tuple[int, int],
    parameters: dict[str, object],
    detail: bool,
    edge_sides: tuple[str, ...],
    seed: int,
) -> Image.Image:
    """Build a visible weave from yarn units; never blend in a source artwork plate."""
    colour_map = source.resize(size, Image.Resampling.NEAREST)
    width, height = size
    pitch_key = "bundle_pitch_detail_px" if detail else "bundle_pitch_overview_px"
    bundle_key = "bundle_size_detail_px" if detail else "bundle_size_overview_px"
    pitch_x, pitch_y = (int(value) for value in parameters[pitch_key])
    bundle_w, bundle_h = (int(value) for value in parameters[bundle_key])
    cross_spacing = int(
        parameters[
            "fine_cross_thread_spacing_detail_px" if detail else "fine_cross_thread_spacing_overview_px"
        ]
    )
    filaments = int(parameters["filaments_per_bundle"])
    ratio = float(parameters["binding_width_ratio"])
    lock_ratio = float(parameters["binding_lock_line_ratio"])
    rng = random.Random(seed)
    surface = Image.new("RGB", size, (104, 96, 84))
    draw = ImageDraw.Draw(surface, "RGBA")

    # Fine cross and anchor threads establish a shared woven field before the
    # coloured bundles are placed. Every colour is sampled only at yarn units.
    for y in range(0, height, cross_spacing):
        for x in range(-4, width + 5, pitch_x):
            colour = sample_colour(colour_map, x + pitch_x / 2, y)
            draw.line(
                (x, y, x + pitch_x, y + rng.choice((-1, 0, 1))),
                fill=(*mix(darken(colour, 0.48), (212, 205, 187), 0.22), 150),
                width=1,
            )
    for x in range(0, width, max(3, pitch_x // 3)):
        for y in range(0, height, pitch_y):
            colour = sample_colour(colour_map, x, y + pitch_y / 2)
            draw.line((x, y, x, y + pitch_y), fill=(*darken(colour, 0.58), 100), width=1)

    for row, y in enumerate(range(-bundle_h, height + bundle_h, pitch_y)):
        offset = pitch_x // 2 if row % 2 else 0
        for x in range(-bundle_w, width + bundle_w, pitch_x):
            cx = x + offset + rng.uniform(-0.8, 0.8)
            cy = y + rng.uniform(-0.8, 0.8)
            colour = sample_colour(colour_map, cx, cy)
            left = round(cx - bundle_w / 2)
            top = round(cy - bundle_h / 2)
            right = round(cx + bundle_w / 2)
            bottom = round(cy + bundle_h / 2)
            draw.rounded_rectangle(
                (left + 1, top + 2, right + 1, bottom + 2),
                radius=max(2, bundle_w // 3),
                fill=(*darken(colour, 0.55), 110),
            )
            body = mix(colour, (245, 238, 216), 0.10)
            draw.rounded_rectangle(
                (left, top, right, bottom),
                radius=max(2, bundle_w // 3),
                fill=(*body, 235),
            )
            for filament in range(filaments):
                horizontal = left + 2 + (right - left - 4) * filament / max(1, filaments - 1)
                wobble = rng.uniform(-0.8, 0.8)
                line_colour = mix(body, (255, 250, 232), 0.50) if filament in {2, 3, 4} else darken(body, 0.66)
                draw.line(
                    (
                        horizontal + wobble,
                        top + 2,
                        horizontal - wobble,
                        cy,
                        horizontal + wobble * 0.5,
                        bottom - 2,
                    ),
                    fill=(*line_colour, 150 if filament in {2, 3, 4} else 105),
                    width=1,
                )
            draw.line(
                (left + 2, cy - bundle_h * 0.20, right - 2, cy - bundle_h * 0.20),
                fill=(*mix(body, (255, 250, 235), 0.68), 70),
                width=1,
            )

    draw_binding(surface, colour_map, width, height, ratio, lock_ratio, edge_sides)
    return surface


def make_overview(source: Image.Image, parameters: dict[str, object]) -> Image.Image:
    canvas_size = (1500, 1900)
    surface = synthesize_surface(source, (1120, 1720), parameters, False, ("left", "right", "top", "bottom"), 9201)
    background = draw_backdrop(canvas_size, 9202)
    destination = [(224, 112), (1276, 112), (1342, 1780), (158, 1780)]
    warped, mask = warp_plane(surface, canvas_size, destination)
    shadow = ImageChops.offset(mask.filter(ImageFilter.GaussianBlur(14)), 9, 14)
    shadow = ImageChops.multiply(shadow, Image.new("L", canvas_size, 88))
    background.paste(Image.new("RGB", canvas_size, (10, 13, 18)), (0, 0), shadow)
    background.paste(warped, (0, 0), mask)
    return background


def crop_for_corner(source: Image.Image) -> Image.Image:
    left, top, right, bottom = DETAIL_BOX
    return source.crop(
        (round(source.width * left), round(source.height * top), round(source.width * right), round(source.height * bottom))
    )


def make_detail(source: Image.Image, parameters: dict[str, object]) -> Image.Image:
    canvas_size = (1500, 1200)
    crop = crop_for_corner(source)
    surface = synthesize_surface(crop, (1320, 965), parameters, True, ("left", "bottom"), 9301)
    background = draw_backdrop(canvas_size, 9302)
    destination = [(130, 78), (1355, 124), (1450, 1130), (64, 1092)]
    warped, mask = warp_plane(surface, canvas_size, destination)
    shadow = ImageChops.offset(mask.filter(ImageFilter.GaussianBlur(12)), 9, 14)
    shadow = ImageChops.multiply(shadow, Image.new("L", canvas_size, 96))
    background.paste(Image.new("RGB", canvas_size, (9, 12, 16)), (0, 0), shadow)
    background.paste(warped, (0, 0), mask)
    return background


def run_checked(command: list[str]) -> dict[str, object]:
    process = subprocess.run(command, check=False, capture_output=True, text=True, encoding="utf-8")
    try:
        report: object = json.loads(process.stdout)
    except json.JSONDecodeError:
        report = {"stdout": process.stdout, "stderr": process.stderr}
    if process.returncode:
        raise RuntimeError(f"command failed: {' '.join(command)}\n{process.stdout}\n{process.stderr}")
    return {"command": command, "result": report}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("design_source", type=Path)
    parser.add_argument("out_dir", type=Path)
    parser.add_argument("--calibration", type=Path, default=DEFAULT_CALIBRATION)
    args = parser.parse_args()

    source_path = args.design_source.resolve()
    out_dir = args.out_dir.resolve()
    calibration_path = args.calibration.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    calibration = json.loads(calibration_path.read_text(encoding="utf-8"))
    parameters = calibration["calibrated_visual_parameters"]

    pair_check = run_checked([sys.executable, str(ROOT / "scripts" / "validate_paired_mappings.py"), "--manifest", str(calibration_path)])
    controls_dir = out_dir / "controls"
    run_checked([sys.executable, str(ROOT / "scripts" / "prepare_design_controls.py"), str(source_path), str(controls_dir)])

    with Image.open(source_path) as loaded:
        source = loaded.convert("RGB")
    proof_path = out_dir / "structure_proof.png"
    source.save(proof_path, format="PNG")
    topology = run_checked([sys.executable, str(ROOT / "scripts" / "validate_topology.py"), str(source_path), str(proof_path), "--aligned"])

    detail_corner = "lower_left"
    lock = {
        "render_backend": "local_deterministic_structure_proof",
        "backend_strategy": "diagnostic_structure_proof",
        "topology_mode": "strict",
        "pattern_control": "deterministic",
        "surface_build_mode": "unavailable",
        "reference_strength": "none",
        "material_id": calibration["material_id"],
        "calibration_manifest": str(calibration_path),
        "calibration_manifest_sha256": sha256(calibration_path),
        "paired_mapping_check": pair_check,
        "source": str(source_path),
        "source_sha256": sha256(source_path),
        "detail_corner": detail_corner,
        "structure_proof": str(proof_path),
        "topology_verification": topology,
        "material_detail": None,
        "detail_review": "not_applicable_proof_only",
        "product_overview": None,
        "delivery_status": "structure_proof_only",
        "warning": "Use the unified image-generation route with the complete design, declared camera anchor, and declared micro construction anchor for user-facing visuals.",
        "colour_authority": "design_source",
    }
    lock_path = out_dir / "render_lock.json"
    lock_path.write_text(json.dumps(lock, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(lock, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
