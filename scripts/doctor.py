#!/usr/bin/env python3
"""Validate the pinned local ComfyUI/PyTorch runtime and print JSON evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runtime-root", default=r"D:\AI\carpet-visualizer-runtime")
    parser.add_argument("--verify-model-hash", action="store_true")
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parents[1]
    lock = json.loads((project_root / "config" / "runtime-lock.json").read_text(encoding="utf-8"))
    runtime_root = Path(args.runtime_root).resolve()
    comfy_root = runtime_root / "ComfyUI"
    models = lock["models"]
    model_reports = []
    for model in models:
        path = comfy_root / Path(model["relative_path"])
        item = {"id": model["id"], "path": str(path), "exists": path.is_file()}
        if args.verify_model_hash and path.is_file():
            item["sha256"] = sha256(path)
            item["hash_matches"] = item["sha256"].lower() == model["sha256"].lower()
        model_reports.append(item)
    node_reports = []
    for node in lock.get("custom_nodes", []):
        path = comfy_root / "custom_nodes" / node["directory"]
        item = {"id": node["id"], "path": str(path), "exists": path.is_dir()}
        if item["exists"]:
            try:
                item["commit"] = subprocess.check_output(
                    ["git", "-C", str(path), "rev-parse", "HEAD"], text=True
                ).strip()
                item["commit_matches"] = item["commit"] == node["commit"]
            except Exception as exc:
                item["error"] = repr(exc)
        node_reports.append(item)

    report: dict[str, object] = {
        "ok": False,
        "platform": platform.platform(),
        "python": sys.version.split()[0],
        "runtime_root": str(runtime_root),
        "runtime_on_d_drive": runtime_root.drive.upper() == "D:",
        "comfyui_exists": (comfy_root / "main.py").is_file(),
        "models": model_reports,
        "custom_nodes": node_reports,
    }

    try:
        import torch

        report.update(
            torch_version=torch.__version__,
            cuda_available=torch.cuda.is_available(),
            cuda_runtime=torch.version.cuda,
        )
        if torch.cuda.is_available():
            probe = torch.ones((512, 512), device="cuda", dtype=torch.float16)
            result = probe @ probe
            torch.cuda.synchronize()
            report.update(
                gpu_name=torch.cuda.get_device_name(0),
                gpu_capability=list(torch.cuda.get_device_capability(0)),
                gpu_probe=float(result[0, 0].item()),
            )
    except Exception as exc:  # diagnostic output must survive import/runtime errors
        report["torch_error"] = repr(exc)

    if report["comfyui_exists"]:
        try:
            report["comfyui_commit"] = subprocess.check_output(
                ["git", "-C", str(comfy_root), "rev-parse", "HEAD"], text=True
            ).strip()
        except Exception as exc:
            report["comfyui_commit_error"] = repr(exc)

    report["ok"] = bool(
        report.get("comfyui_exists")
        and all(item["exists"] and (not args.verify_model_hash or item.get("hash_matches")) for item in model_reports)
        and all(item["exists"] and item.get("commit_matches") for item in node_reports)
        and report.get("cuda_available")
        and report.get("gpu_probe") == 512.0
        and report.get("comfyui_commit") == lock["comfyui"]["commit"]
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
