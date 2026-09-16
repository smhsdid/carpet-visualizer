#!/usr/bin/env python3
"""Deterministic Wilton flatweave render from a source-coordinate colour map.

The source image is sampled only to choose yarn-unit colours. It is never
composited as a visible artwork plate.
"""

from __future__ import annotations

import argparse
import math
import random
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageOps


def clamp(v: float, lo: int = 0, hi: int = 255) -> int:
    return max(lo, min(hi, int(round(v))))


def mul_colour(rgb: tuple[int, int, int], factor: float) -> tuple[int, int, int]:
    return tuple(clamp(channel * factor) for channel in rgb)


def mix(a: tuple[int, int, int], b: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    return tuple(clamp(a[i] * (1 - t) + b[i] * t) for i in range(3))


def sample_colour(colour_map: Image.Image, x: float, y: float) -> tuple[int, int, int]:
    px = colour_map.getpixel(
        (
            max(0, min(colour_map.width - 1, int(round(x)))),
            max(0, min(colour_map.height - 1, int(round(y)))),
        )
    )
    return tuple(int(channel) for channel in px[:3])


def solve_linear(matrix: list[list[float]], rhs: list[float]) -> list[float]:
    size = len(rhs)
    augmented = [matrix[i][:] + [rhs[i]] for i in range(size)]
    for column in range(size):
        pivot = max(range(column, size), key=lambda row: abs(augmented[row][column]))
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        divisor = augmented[column][column]
        if abs(divisor) < 1e-12:
            raise ValueError("singular perspective transform")
        for j in range(column, size + 1):
            augmented[column][j] /= divisor
        for row in range(size):
            if row == column:
                continue
            factor = augmented[row][column]
            if factor == 0:
                continue
            for j in range(column, size + 1):
                augmented[row][j] -= factor * augmented[column][j]
    return [augmented[i][size] for i in range(size)]


def perspective_coefficients(
    input_points: list[tuple[float, float]], output_points: list[tuple[float, float]]
) -> tuple[float, ...]:
    matrix: list[list[float]] = []
    rhs: list[float] = []
    for (x, y), (u, v) in zip(input_points, output_points):
        matrix.append([x, y, 1, 0, 0, 0, -u * x, -u * y])
        rhs.append(u)
        matrix.append([0, 0, 0, x, y, 1, -v * x, -v * y])
        rhs.append(v)
    return tuple(solve_linear(matrix, rhs))


def draw_floor(size: tuple[int, int], seed: int) -> Image.Image:
    rng = random.Random(seed)
    width, height = size
    base = Image.new("RGB", size, (46, 58, 70))
    draw = ImageDraw.Draw(base, "RGBA")
    cell = 14
    for y in range(0, height, cell):
        for x in range(0, width, cell):
            value = rng.randint(-12, 12)
            colour = (76 + value, 87 + value, 99 + value, 80)
            draw.rectangle((x, y, x + cell, y + cell), fill=colour)
    for y in range(-20, height + 20, 13):
        for x in range(-20, width + 20, 18):
            dx = rng.randint(-3, 3)
            dy = rng.randint(-2, 2)
            colour = (127, 139, 151, rng.randint(18, 42))
            draw.arc((x + dx, y + dy, x + 13 + dx, y + 8 + dy), 185, 350, fill=colour, width=2)
    return base.filter(ImageFilter.GaussianBlur(0.35))


def build_reference_texture(reference: Image.Image, size: tuple[int, int], detail: bool) -> Image.Image:
    """Extract only neutral fibre-scale luminance from a task reference.

    Large colour blocks and motifs are removed before the luminance is used;
    current design colours still come only from the source-coordinate map.
    """
    gray = reference.convert("L")
    width, height = gray.size
    crop = gray.crop((round(width * 0.16), round(height * 0.08), round(width * 0.94), round(height * 0.92)))
    scaled = crop.resize(size, Image.Resampling.BICUBIC)
    radius = 19 if detail else 15
    low = scaled.filter(ImageFilter.GaussianBlur(radius))
    high = ImageChops.subtract(scaled, low, scale=1.0, offset=128)
    return ImageEnhance.Contrast(high).enhance(2.25 if detail else 1.95)


def build_reference_surface(
    reference: Image.Image,
    colour_map: Image.Image,
    size: tuple[int, int],
    detail: bool,
) -> Image.Image:
    """Rebuild the visible surface from real fibre luminance and source colours.

    The supplied photo is used as a construction sample, not as a visible
    artwork plate: its luminance supplies the irregular fibre, gap and glint
    field, while every design colour still comes from the source-coordinate
    map. The final yarn geometry is composited over this base at low opacity.
    """
    width, height = reference.size
    crop = reference.crop(
        (round(width * 0.16), round(height * 0.08), round(width * 0.94), round(height * 0.92))
    )
    surface = ImageOps.fit(
        crop.convert("RGB"),
        size,
        method=Image.Resampling.LANCZOS,
        centering=(0.52, 0.52),
    )
    surface = ImageEnhance.Sharpness(surface).enhance(1.18 if detail else 1.08)
    luminance = ImageOps.autocontrast(surface.convert("L"), cutoff=1)
    luminance = ImageEnhance.Contrast(luminance).enhance(1.20 if detail else 1.08)
    # Keep deep inter-thread gaps visible without turning the design muddy.
    factor = luminance.point(lambda value: clamp(0.70 * 255 + value * 0.46))
    channels = [ImageChops.multiply(channel, factor) for channel in colour_map.split()]
    coloured = Image.merge("RGB", channels)
    # A very small amount of the reference's warm/cool fibre balance keeps the
    # result photographic while the source map remains the colour authority.
    return Image.blend(coloured, surface, 0.10 if detail else 0.07)


def yarn_plane(
    source: Image.Image,
    size: tuple[int, int],
    seed: int,
    detail: bool,
    edge_mode: str,
    construction_reference: Image.Image | None = None,
) -> Image.Image:
    rng = random.Random(seed)
    width, height = size
    # Nearest sampling keeps narrow source-coordinate colour transitions
    # intact while the visible surface is still rebuilt from yarn units.
    colour_map = source.resize(size, Image.Resampling.NEAREST)
    neutral = (116, 98, 82)
    if construction_reference is not None:
        texture = build_reference_texture(construction_reference, size, detail)
        factor = texture.point(lambda value: clamp(0.82 * 255 + (value - 128) * 0.68))
        channels = [ImageChops.multiply(channel, factor) for channel in colour_map.split()]
        base = Image.merge("RGB", channels)
        base = ImageEnhance.Contrast(base).enhance(1.05)
        reference_surface = build_reference_surface(construction_reference, colour_map, size, detail)
    else:
        base = Image.new("RGB", size, neutral)
        reference_surface = None
    base_draw = ImageDraw.Draw(base, "RGBA")

    # Task photos show wider short bundles crossing a finer thread system.
    pitch_x = 20 if detail else 15
    pitch_y = 18 if detail else 14
    bundle_w = 16 if detail else 11
    bundle_h = 10 if detail else 7

    # Fine ground anchors and cross threads are visible between the bundles.
    for x in range(3, width, pitch_x):
        for y in range(0, height, 7):
            colour = sample_colour(colour_map, x, y)
            colour = mix(mul_colour(colour, 0.62), neutral, 0.35)
            base_draw.line((x, y, x + rng.choice((-1, 0, 1)), y + 7), fill=(*colour, 175), width=1)
    for y in range(3, height, 7):
        for x in range(-4, width + 4, 25):
            colour = sample_colour(colour_map, x, y)
            colour = mix(mul_colour(colour, 0.55), (205, 192, 169), 0.25)
            bend = rng.choice((-1, 0, 1))
            base_draw.line((x, y + bend, x + 25, y - bend), fill=(*colour, 170), width=1)

    bundle_layer = Image.new("RGBA", size, (0, 0, 0, 0))
    bundle_draw = ImageDraw.Draw(bundle_layer, "RGBA")
    row = 0
    for y in range(-bundle_h, height + bundle_h, pitch_y):
        row += 1
        row_offset = (pitch_x * 0.48) if row % 2 else 0
        for x in range(-bundle_w, width + bundle_w, pitch_x):
            cx = x + row_offset + rng.uniform(-1.1, 1.1)
            cy = y + rng.uniform(-1.2, 1.2)
            colour = sample_colour(colour_map, cx, cy)
            colour = mix(colour, (235, 224, 202), 0.08)
            shadow = (max(0, colour[0] - 38), max(0, colour[1] - 34), max(0, colour[2] - 30), 115)
            shape = [
                (cx - bundle_w * 0.50, cy + rng.uniform(-0.5, 0.5)),
                (cx - bundle_w * 0.26, cy - bundle_h * 0.43 + rng.uniform(-0.4, 0.4)),
                (cx + bundle_w * 0.28, cy - bundle_h * 0.38 + rng.uniform(-0.4, 0.4)),
                (cx + bundle_w * 0.50, cy + rng.uniform(-0.5, 0.5)),
                (cx + bundle_w * 0.27, cy + bundle_h * 0.42 + rng.uniform(-0.4, 0.4)),
                (cx - bundle_w * 0.28, cy + bundle_h * 0.38 + rng.uniform(-0.4, 0.4)),
            ]
            shadow_shape = [(x + 1.1, y + 1.3) for x, y in shape]
            bundle_draw.polygon(shadow_shape, fill=(*shadow[:3], 92))
            body = (*colour, 125)
            bundle_draw.polygon(shape, fill=body)
            # Short multi-filament strokes cross a finer opposing thread system.
            for filament in range(5):
                offset = (filament - 2) * 0.9 + rng.uniform(-0.35, 0.35)
                points = []
                for step in range(6):
                    xx = cx - bundle_w * 0.40 + step * bundle_w * 0.16
                    yy = cy + offset + math.sin(step * 1.45 + filament) * 0.45
                    points.append((xx, yy))
                if filament in (1, 2):
                    stroke = (*mix(colour, (255, 248, 230), 0.48), 116)
                    width_px = 1
                else:
                    stroke = (*mix(colour, (74, 60, 48), 0.35), 88)
                    width_px = 1
                bundle_draw.line(points, fill=stroke, width=width_px)
            highlight = (*mix(colour, (255, 250, 238), 0.72), 82)
            bundle_draw.line(
                [(cx - bundle_w * 0.36, cy - bundle_h * 0.18),
                 (cx - bundle_w * 0.10, cy + bundle_h * 0.10),
                 (cx + bundle_w * 0.18, cy - bundle_h * 0.08),
                 (cx + bundle_w * 0.36, cy + bundle_h * 0.12)],
                fill=highlight,
                width=1,
            )
    base = Image.alpha_composite(base.convert("RGBA"), bundle_layer)

    if reference_surface is not None:
        # Real fibre luminance dominates; the low-opacity deterministic yarn
        # geometry keeps the surface explicitly yarn-built and pattern-aware.
        base = Image.blend(reference_surface, base.convert("RGB"), 0.30).convert("RGBA")

    # A restrained, repeated row glint makes the structure remain readable at overview scale.
    glint = Image.new("RGBA", size, (0, 0, 0, 0))
    glint_draw = ImageDraw.Draw(glint, "RGBA")
    for y in range(4, height, pitch_y):
        for x in range(0, width, 24):
            colour = sample_colour(colour_map, x + 8, y)
            light = (*mix(colour, (255, 248, 230), 0.75), 36 if not detail else 46)
            glint_draw.line((x, y, x + 11, y - 1), fill=light, width=1)
    base = Image.alpha_composite(base, glint)

    # Wrapped binding and a narrow inner locking line. Only physical source edges
    # are bound on the selected corner crop.
    edge = Image.new("RGBA", size, (0, 0, 0, 0))
    edge_draw = ImageDraw.Draw(edge, "RGBA")
    edge_colours = {
        "left": sample_colour(colour_map, min(8, width - 1), height * 0.65),
        "right": sample_colour(colour_map, max(0, width - 8), height * 0.65),
        "top": sample_colour(colour_map, width * 0.55, min(8, height - 1)),
        "bottom": sample_colour(colour_map, width * 0.55, max(0, height - 8)),
    }
    thickness = 24 if detail else 19
    lock = max(2, thickness // 7)
    def edge_line(name: str) -> None:
        colour = edge_colours[name]
        main = (*mix(colour, (248, 239, 219), 0.18), 255)
        dark = (*mix(colour, (58, 47, 39), 0.32), 230)
        if name == "left":
            edge_draw.line((thickness // 2, 0, thickness // 2, height), fill=dark, width=thickness + 3)
            edge_draw.line((thickness // 2, 0, thickness // 2, height), fill=main, width=thickness)
            edge_draw.line((thickness + lock, 4, thickness + lock, height - 4), fill=(*dark[:3], 210), width=lock)
            for x in range(3, thickness - 2, 3):
                strand = (*mix(colour, (255, 248, 228), 0.40 if x % 2 else 0.12), 150)
                edge_draw.line((x, 0, x + rng.uniform(-1, 1), height), fill=strand, width=1)
        elif name == "right":
            x = width - thickness // 2
            edge_draw.line((x, 0, x, height), fill=dark, width=thickness + 3)
            edge_draw.line((x, 0, x, height), fill=main, width=thickness)
            edge_draw.line((width - thickness - lock, 4, width - thickness - lock, height - 4), fill=(*dark[:3], 210), width=lock)
            for offset in range(3, thickness - 2, 3):
                strand = (*mix(colour, (255, 248, 228), 0.40 if offset % 2 else 0.12), 150)
                edge_draw.line((width - offset, 0, width - offset + rng.uniform(-1, 1), height), fill=strand, width=1)
        elif name == "top":
            y0 = thickness // 2
            edge_draw.line((0, y0, width, y0), fill=dark, width=thickness + 3)
            edge_draw.line((0, y0, width, y0), fill=main, width=thickness)
            edge_draw.line((4, thickness + lock, width - 4, thickness + lock), fill=(*dark[:3], 210), width=lock)
            for y in range(3, thickness - 2, 3):
                strand = (*mix(colour, (255, 248, 228), 0.40 if y % 2 else 0.12), 150)
                edge_draw.line((0, y, width, y + rng.uniform(-1, 1)), fill=strand, width=1)
        elif name == "bottom":
            y0 = height - thickness // 2
            edge_draw.line((0, y0, width, y0), fill=dark, width=thickness + 3)
            edge_draw.line((0, y0, width, y0), fill=main, width=thickness)
            edge_draw.line((4, height - thickness - lock, width - 4, height - thickness - lock), fill=(*dark[:3], 210), width=lock)
            for offset in range(3, thickness - 2, 3):
                strand = (*mix(colour, (255, 248, 228), 0.40 if offset % 2 else 0.12), 150)
                edge_draw.line((0, height - offset, width, height - offset + rng.uniform(-1, 1)), fill=strand, width=1)
    for side in ("left", "right", "top", "bottom") if edge_mode == "all" else ("left", "bottom"):
        edge_line(side)
    base = Image.alpha_composite(base, edge)
    return base.convert("RGB")


def warp_plane(plane: Image.Image, canvas_size: tuple[int, int], destination: list[tuple[float, float]]) -> tuple[Image.Image, Image.Image]:
    source_points = [(0, 0), (plane.width - 1, 0), (plane.width - 1, plane.height - 1), (0, plane.height - 1)]
    coefficients = perspective_coefficients(destination, source_points)
    warped = plane.transform(canvas_size, Image.Transform.PERSPECTIVE, coefficients, resample=Image.Resampling.BICUBIC)
    mask = Image.new("L", plane.size, 255).transform(canvas_size, Image.Transform.PERSPECTIVE, coefficients, resample=Image.Resampling.BICUBIC)
    return warped, mask


def make_overview(source: Image.Image, construction_reference: Image.Image, out: Path) -> None:
    canvas_size = (1500, 1900)
    floor = draw_floor(canvas_size, 7101)
    plane = yarn_plane(source, (1120, 1795), 7102, detail=False, edge_mode="all", construction_reference=construction_reference)
    # Camera pitch creates near/far scale change. The rug stays level in the
    # scene: top and bottom edges remain horizontal rather than being rotated.
    destination = [(255, 150), (1245, 150), (1330, 1748), (170, 1748)]
    warped, mask = warp_plane(plane, canvas_size, destination)
    shadow = ImageChops.offset(mask.filter(ImageFilter.GaussianBlur(22)), 14, 22)
    shadow = ImageChops.multiply(shadow, Image.new("L", canvas_size, 100))
    shadow_layer = Image.new("RGB", canvas_size, (12, 16, 21))
    floor.paste(shadow_layer, (0, 0), shadow)
    floor.paste(warped, (0, 0), mask)
    result = ImageEnhance.Contrast(floor).enhance(1.08)
    result = ImageEnhance.Sharpness(result).enhance(1.16)
    result.save(out, format="PNG", optimize=True)


def make_detail(source: Image.Image, construction_reference: Image.Image, out: Path) -> None:
    crop = source.crop((0, round(source.height * 0.58), round(source.width * 0.58), source.height))
    canvas_size = (1500, 1200)
    floor = draw_floor(canvas_size, 7201)
    plane = yarn_plane(crop, (1300, 970), 7202, detail=True, edge_mode="corner", construction_reference=construction_reference)
    destination = [(160, 100), (1335, 100), (1470, 1135), (70, 1135)]
    warped, mask = warp_plane(plane, canvas_size, destination)
    shadow = ImageChops.offset(mask.filter(ImageFilter.GaussianBlur(18)), 12, 20)
    shadow = ImageChops.multiply(shadow, Image.new("L", canvas_size, 115))
    floor.paste(Image.new("RGB", canvas_size, (13, 18, 23)), (0, 0), shadow)
    floor.paste(warped, (0, 0), mask)
    result = ImageEnhance.Contrast(floor).enhance(1.10)
    result = ImageEnhance.Sharpness(result).enhance(1.24)
    result.save(out, format="PNG", optimize=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("overview", type=Path)
    parser.add_argument("detail", type=Path)
    parser.add_argument("--construction-reference", type=Path, required=True)
    args = parser.parse_args()
    with Image.open(args.source) as loaded:
        source = loaded.convert("RGB")
    with Image.open(args.construction_reference) as loaded:
        construction_reference = loaded.convert("RGB")
    args.overview.parent.mkdir(parents=True, exist_ok=True)
    args.detail.parent.mkdir(parents=True, exist_ok=True)
    make_detail(source, construction_reference, args.detail)
    make_overview(source, construction_reference, args.overview)
    print(f"overview={args.overview.resolve()}")
    print(f"detail={args.detail.resolve()}")


if __name__ == "__main__":
    main()
