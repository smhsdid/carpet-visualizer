#!/usr/bin/env python3
"""Submit the bundled SDXL img2img workflow to a running ComfyUI server."""

from __future__ import annotations

import argparse
import json
import shutil
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path

from PIL import Image, ImageOps


POSITIVE = (
    "photorealistic directly overhead studio product photograph of the supplied complete rug, "
    "preserve the exact artwork, motif topology, color regions, outline and orientation, "
    "a real thin relief-rich woven jacquard carpet rather than flat artwork, "
    "dense fine interlaced yarns visibly cover every colored region including the large plain center, "
    "short raised vertical yarn crowns cross fine horizontal threads, subtle irregular fibre fuzz, "
    "compact woven micro-relief and tiny self shadows remain visible at full product scale, "
    "narrow rounded serged binding with a slight physical edge shadow, "
    "bright clean commercial product lighting, crisp textile detail, high resolution"
)
NEGATIVE = (
    "changed pattern, extra motif, missing motif, warped outline, perspective view, folded rug, "
    "cropped rug, text, watermark, flat vector artwork, illustration, perfectly flat color fill, "
    "smooth printed surface, textureless center, fur, shag, chunky knit, rope, plastic, blurry"
)


def request_json(url: str, payload: dict | None = None) -> dict:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=data)
    if data is not None:
        request.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def prepare_input(source: Path, destination: Path, max_side: int) -> None:
    with Image.open(source) as opened:
        image = ImageOps.exif_transpose(opened).convert("RGB")
        scale = min(1.0, max_side / max(image.size))
        width = max(64, round(image.width * scale / 64) * 64)
        height = max(64, round(image.height * scale / 64) * 64)
        image = image.resize((width, height), Image.Resampling.LANCZOS)
        image.save(destination, quality=96)


def workflow(image_name: str, checkpoint: str, seed: int, denoise: float, steps: int) -> dict:
    return {
        "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": checkpoint}},
        "2": {"class_type": "LoadImage", "inputs": {"image": image_name}},
        "3": {"class_type": "CLIPTextEncode", "inputs": {"text": POSITIVE, "clip": ["1", 1]}},
        "4": {"class_type": "CLIPTextEncode", "inputs": {"text": NEGATIVE, "clip": ["1", 1]}},
        "5": {"class_type": "VAEEncode", "inputs": {"pixels": ["2", 0], "vae": ["1", 2]}},
        "6": {
            "class_type": "KSampler",
            "inputs": {
                "seed": seed,
                "steps": steps,
                "cfg": 5.5,
                "sampler_name": "dpmpp_2m",
                "scheduler": "karras",
                "denoise": denoise,
                "model": ["1", 0],
                "positive": ["3", 0],
                "negative": ["4", 0],
                "latent_image": ["5", 0]
            }
        },
        "7": {"class_type": "VAEDecode", "inputs": {"samples": ["6", 0], "vae": ["1", 2]}},
        "8": {
            "class_type": "SaveImage",
            "inputs": {"filename_prefix": "carpet-visualizer/overview", "images": ["7", 0]}
        }
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--runtime-root", default=r"D:\AI\carpet-visualizer-runtime")
    parser.add_argument("--output-dir", type=Path, default=Path("output"))
    parser.add_argument("--server", default="http://127.0.0.1:8188")
    parser.add_argument("--checkpoint", default="sd_xl_base_1.0.safetensors")
    parser.add_argument("--seed", type=int, default=5060001)
    parser.add_argument("--steps", type=int, default=14)
    parser.add_argument("--denoise", type=float, default=0.28)
    parser.add_argument("--max-side", type=int, default=1024)
    parser.add_argument("--timeout", type=int, default=900)
    args = parser.parse_args()

    source = args.input.resolve()
    if not source.is_file():
        raise SystemExit(f"Input image not found: {source}")
    comfy_root = Path(args.runtime_root).resolve() / "ComfyUI"
    input_dir = comfy_root / "input"
    input_dir.mkdir(parents=True, exist_ok=True)
    prepared_name = f"carpet_visualizer_{uuid.uuid4().hex}.jpg"
    prepared_path = input_dir / prepared_name
    prepare_input(source, prepared_path, args.max_side)

    try:
        result = request_json(
            f"{args.server}/prompt",
            {"prompt": workflow(prepared_name, args.checkpoint, args.seed, args.denoise, args.steps)},
        )
        prompt_id = result["prompt_id"]
        deadline = time.monotonic() + args.timeout
        history = None
        while time.monotonic() < deadline:
            current = request_json(f"{args.server}/history/{prompt_id}")
            if prompt_id in current:
                history = current[prompt_id]
                break
            time.sleep(2)
        if history is None:
            raise TimeoutError(f"ComfyUI job {prompt_id} did not finish in {args.timeout}s")

        images = history.get("outputs", {}).get("8", {}).get("images", [])
        if not images:
            raise RuntimeError(json.dumps(history, ensure_ascii=False)[:2000])
        output_dir = args.output_dir.resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        delivered = []
        for index, item in enumerate(images, start=1):
            generated = comfy_root / "output" / item.get("subfolder", "") / item["filename"]
            destination = output_dir / f"product-overview-{prompt_id[:8]}-{index}.png"
            shutil.copy2(generated, destination)
            delivered.append(str(destination))
        print(json.dumps({"prompt_id": prompt_id, "outputs": delivered}, ensure_ascii=False, indent=2))
        return 0
    finally:
        prepared_path.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
