#!/usr/bin/env python3
"""Enhance an accepted overview with a local ComfyUI super-resolution model."""

from __future__ import annotations

import argparse
import json
import shutil
import time
import uuid
from pathlib import Path

from comfyui_client import request_json


def workflow(image_name: str, model_name: str, scale: float) -> dict:
    return {
        "1": {"class_type": "LoadImage", "inputs": {"image": image_name}},
        "2": {"class_type": "UpscaleModelLoader", "inputs": {"model_name": model_name}},
        "3": {
            "class_type": "ImageUpscaleWithModel",
            "inputs": {"upscale_model": ["2", 0], "image": ["1", 0]},
        },
        "4": {
            "class_type": "ImageScaleBy",
            "inputs": {"image": ["3", 0], "upscale_method": "lanczos", "scale_by": scale / 4.0},
        },
        "5": {
            "class_type": "SaveImage",
            "inputs": {"filename_prefix": "carpet-visualizer/hybrid-enhanced", "images": ["4", 0]},
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--runtime-root", default=r"D:\AI\carpet-visualizer-runtime")
    parser.add_argument("--output-dir", type=Path, default=Path("output"))
    parser.add_argument("--server", default="http://127.0.0.1:8188")
    parser.add_argument("--model", default="RealESRGAN_x4plus.pth")
    parser.add_argument("--scale", type=float, default=2.0)
    parser.add_argument("--timeout", type=int, default=900)
    args = parser.parse_args()
    if not 1.0 <= args.scale <= 4.0:
        raise SystemExit("--scale must be between 1 and 4")

    source = args.input.resolve()
    if not source.is_file():
        raise SystemExit(f"Input image not found: {source}")
    comfy_root = Path(args.runtime_root).resolve() / "ComfyUI"
    input_dir = comfy_root / "input"
    input_dir.mkdir(parents=True, exist_ok=True)
    staged_name = f"hybrid_master_{uuid.uuid4().hex}{source.suffix.lower()}"
    staged_path = input_dir / staged_name
    shutil.copy2(source, staged_path)

    try:
        response = request_json(f"{args.server}/prompt", {"prompt": workflow(staged_name, args.model, args.scale)})
        prompt_id = response["prompt_id"]
        deadline = time.monotonic() + args.timeout
        history = None
        while time.monotonic() < deadline:
            current = request_json(f"{args.server}/history/{prompt_id}")
            if prompt_id in current:
                history = current[prompt_id]
                break
            time.sleep(1)
        if history is None:
            raise TimeoutError(f"ComfyUI job {prompt_id} did not finish in {args.timeout}s")
        images = history.get("outputs", {}).get("5", {}).get("images", [])
        if not images:
            raise RuntimeError(json.dumps(history, ensure_ascii=False)[:2000])

        output_dir = args.output_dir.resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        delivered = []
        for index, item in enumerate(images, start=1):
            generated = comfy_root / "output" / item.get("subfolder", "") / item["filename"]
            destination = output_dir / f"product-overview-hybrid-enhanced-{prompt_id[:8]}-{index}.png"
            shutil.copy2(generated, destination)
            delivered.append(str(destination))
        print(json.dumps({"prompt_id": prompt_id, "scale": args.scale, "outputs": delivered}, ensure_ascii=False, indent=2))
        return 0
    finally:
        staged_path.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
