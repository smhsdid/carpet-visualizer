"""Validate the unified reference packet for Wilton visual generation."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = ROOT / "assets" / "material-library" / "wilton-flatweave-01"
MANIFEST = ASSET_ROOT / "manifest.yaml"
PAIRS = ASSET_ROOT / "paired-mappings.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def manifest_text() -> str:
    return MANIFEST.read_text(encoding="utf-8")


def manifest_value(name: str) -> str:
    match = re.search(rf"(?m)^\s*{re.escape(name)}:\s*(.+?)\s*$", manifest_text())
    if not match:
        raise ValueError(f"missing manifest field: {name}")
    return match.group(1).strip().strip('"')


def validate_asset(path_text: str, expected_hash: str | None = None) -> None:
    path = ASSET_ROOT / path_text
    if not path.is_file():
        raise ValueError(f"missing manifest asset: {path}")
    if expected_hash and sha256(path) != expected_hash.lower():
        raise ValueError(f"manifest hash does not match: {path}")


def validate_manifest() -> None:
    text = manifest_text()
    camera_match = re.search(
        r"(?ms)^detail_camera_anchor:\s*\n\s+path:\s*(quality/accepted-detail-camera-anchor-v1\.jpg)\s*\n\s+sha256:\s*([a-f0-9]+)\s*$",
        text,
    )
    if not camera_match:
        raise ValueError("missing declared generic detail camera anchor")
    validate_asset(camera_match.group(1), camera_match.group(2))

    micro_path = "derived/wilton-unit-micro-anchor-v1.jpg"
    validate_asset(micro_path, "939bc3f2303c31c6380aa0017532951f5eddde4fb373d57d5e51b75048807b56")
    validate_asset("construction/sample-03-overall.jpg")
    validate_asset("quality/accepted-detail-anchor-v1.png")

    if manifest_value("material_reference_budget") != "2":
        raise ValueError("the unified route requires two construction references")
    if manifest_value("detail") != "quality/accepted-detail-camera-anchor-v1.jpg":
        raise ValueError("Wilton detail route must declare the generic camera anchor")
    if "detail_reference_packet: [design_source, detail_camera_anchor, unit_micro_anchor_v1]" not in text:
        raise ValueError("detail packet must contain design, camera anchor, and micro anchor in that order")
    if "overview_reference_packet: [design_source, sample_03_overall, unit_micro_anchor_v1]" not in text:
        raise ValueError("overview packet must contain design, product reference, and micro anchor in that order")
    for field in ("bundle_length_variation", "two_length_classes", "longitudinal_channels", "camera_geometry", "camera_space_registration"):
        if not re.search(rf"(?m)^\s*{field}:", text):
            raise ValueError(f"missing Wilton texture control: {field}")
    quality_controls = re.search(r"(?ms)^quality_anchor:.*?^\s+controls:\s*(\[[^\n]+\])", text)
    if not quality_controls or quality_controls.group(1) != "[exposure, white_balance, product_photography]":
        raise ValueError("quality anchor must control photographic finish only")


def paired_design_hashes() -> dict[str, str]:
    data = json.loads(PAIRS.read_text(encoding="utf-8"))
    return {pair["id"]: pair["design"]["sha256"].lower() for pair in data["pairs"]}


def forbidden_paths_for_source(source_hash: str) -> set[str]:
    data = json.loads(PAIRS.read_text(encoding="utf-8"))
    forbidden: set[str] = set()
    for pair in data["pairs"]:
        if pair["design"]["sha256"].lower() == source_hash.lower():
            forbidden.update({pair["overview"]["path"], pair["detail"]["path"]})
    return forbidden


def validate_lock(lock_path: Path) -> None:
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    source_hash = str(lock.get("source_sha256", "")).lower()
    if not re.fullmatch(r"[a-f0-9]{64}", source_hash):
        raise ValueError("run record must contain source_sha256")
    roles = [attachment.get("role", "") for attachment in lock.get("reference_attachments", [])]
    required = {"design_source_pattern_and_colour_authority", "generic_camera_and_construction_anchor"}
    if not required.issubset(roles):
        raise ValueError(f"run record is missing required attachment roles: {sorted(required - set(roles))}")
    forbidden = forbidden_paths_for_source(source_hash)
    for attachment in lock.get("reference_attachments", []):
        path = str(attachment.get("path", ""))
        if any(path.replace("\\", "/").endswith(item) for item in forbidden):
            raise ValueError(f"matching paired reference is forbidden: {path}")
        declared_hash = str(attachment.get("sha256", "")).lower()
        if not re.fullmatch(r"[a-f0-9]{64}", declared_hash):
            raise ValueError(f"attachment is missing sha256: {path}")
        attachment_path = Path(path)
        if not attachment_path.is_file():
            attachment_path = ASSET_ROOT / path.replace("\\", "/")
        if not attachment_path.is_file():
            raise ValueError(f"attachment path does not resolve: {path}")
        if sha256(attachment_path) != declared_hash:
            raise ValueError(f"attachment SHA-256 does not match: {path}")
    prompts = lock.get("final_prompts")
    if not isinstance(prompts, dict) or not prompts.get("detail") or not prompts.get("overview"):
        raise ValueError("run record must contain final detail and overview prompts")
    if not isinstance(lock.get("generation_parameters"), dict):
        raise ValueError("run record must contain generation_parameters")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lock", type=Path)
    parser.add_argument("--design", type=Path, help="check the source hash against paired-reference exclusions")
    args = parser.parse_args()
    validate_manifest()
    result = {"status": "pass", "manifest": str(MANIFEST), "lock_checked": bool(args.lock), "route": "unified_reference_grounded_generation"}
    if args.design:
        current_hash = sha256(args.design)
        result["source_sha256"] = current_hash
        result["forbidden_paired_paths"] = sorted(forbidden_paths_for_source(current_hash))
    if args.lock:
        validate_lock(args.lock)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
