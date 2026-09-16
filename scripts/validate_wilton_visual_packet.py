"""Validate reference packets for Wilton visual previews."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "assets" / "material-library" / "wilton-flatweave-01" / "manifest.yaml"
ASSET_ROOT = MANIFEST.parent


def manifest_value(name: str) -> str:
    match = re.search(rf"(?m)^\s*{re.escape(name)}:\s*(.+?)\s*$", MANIFEST.read_text(encoding="utf-8"))
    if not match:
        raise ValueError(f"missing manifest field: {name}")
    return match.group(1).strip().strip('"')


def expect_packet(text: str, key: str) -> None:
    expected = "[design_source, accepted_detail_camera_anchor_v1, unit_micro_anchor_v1]" if key == "detail_reference_packet" else "[design_source, unit_micro_anchor_v1]"
    matches = re.findall(rf"(?m)^\s*{re.escape(key)}:\s*(.+?)\s*$", text)
    if not matches:
        raise ValueError(f"missing manifest field: {key}")
    actual = matches[-1].strip().strip('"')
    if actual != expected:
        raise ValueError(f"{key} must be {expected}, got {actual}")


def validate_manifest() -> None:
    anchor_match = re.search(
        r"(?ms)^quality_anchor:\s*\n\s+path:\s*(quality/accepted-detail-anchor-v1\.png)\s*\n\s+sha256:\s*([a-f0-9]+)\s*$",
        MANIFEST.read_text(encoding="utf-8"),
    )
    if not anchor_match:
        raise ValueError("missing declared accepted quality anchor")
    anchor = ASSET_ROOT / anchor_match.group(1)
    if not anchor.is_file():
        raise ValueError(f"missing quality-anchor asset: {anchor}")
    expected_hash = anchor_match.group(2)
    actual_hash = hashlib.sha256(anchor.read_bytes()).hexdigest()
    if actual_hash != expected_hash:
        raise ValueError("quality-anchor SHA-256 does not match manifest")
    camera_match = re.search(
        r"(?ms)^detail_camera_anchor:\s*\n\s+path:\s*(quality/accepted-detail-camera-anchor-v1\.jpg)\s*\n\s+sha256:\s*([a-f0-9]+)\s*$",
        MANIFEST.read_text(encoding="utf-8"),
    )
    if not camera_match:
        raise ValueError("missing declared real detail camera anchor")
    camera_anchor = ASSET_ROOT / camera_match.group(1)
    if not camera_anchor.is_file() or hashlib.sha256(camera_anchor.read_bytes()).hexdigest() != camera_match.group(2):
        raise ValueError("detail-camera anchor SHA-256 does not match manifest")
    if manifest_value("material_reference_budget") != "2":
        raise ValueError("unmatched Wilton detail route requires camera + micro construction anchors")
    if manifest_value("detail") != "construction/sample-02-detail-c.jpg":
        raise ValueError("Wilton detail route must declare the paired material detail")
    manifest_text = MANIFEST.read_text(encoding="utf-8")
    micro_anchor = ASSET_ROOT / "derived" / "wilton-unit-micro-anchor-v1.jpg"
    if not micro_anchor.is_file():
        raise ValueError("missing Wilton multi-unit micro construction anchor")
    if hashlib.sha256(micro_anchor.read_bytes()).hexdigest() != "939bc3f2303c31c6380aa0017532951f5eddde4fb373d57d5e51b75048807b56":
        raise ValueError("Wilton multi-unit micro construction anchor hash does not match")
    for field in ("bundle_length_variation", "two_length_classes", "longitudinal_channels", "camera_geometry", "camera_space_registration"):
        if not re.search(rf"(?m)^\s*{field}:", manifest_text):
            raise ValueError(f"missing Wilton texture control: {field}")
    expect_packet(MANIFEST.read_text(encoding="utf-8"), "detail_reference_packet")
    expect_packet(MANIFEST.read_text(encoding="utf-8"), "overview_reference_packet")
    override_match = re.search(
        r"(?ms)^paired_mapping_overrides:\s*\n\s+sample_02:\s*\n\s+source_sha256:\s*([a-f0-9]+).*?"
        r"^\s+detail_reference_packet:\s*(\[[^\n]+\]).*?"
        r"^\s+required_omissions:\s*(\[[^\n]+\])",
        manifest_text,
    )
    if not override_match:
        raise ValueError("missing sample-02 exact-paired override")
    if override_match.group(1) != "8cf1cad996defe75a0061aa879ed21080d79ec936cbf51ddf06460a25f71c4a3":
        raise ValueError("sample-02 override has an unexpected source hash")
    if override_match.group(2) != "[design_source, paired_product_overview, paired_material_detail]":
        raise ValueError("sample-02 override has an unexpected detail packet")
    if override_match.group(3) != "[accepted_quality_anchor, unit_micro_anchor]":
        raise ValueError("sample-02 override must omit conflicting generic anchors")
    quality_controls = re.search(r"(?ms)^quality_anchor:.*?^\s+controls:\s*(\[[^\n]+\])", manifest_text)
    if not quality_controls or quality_controls.group(1) != "[exposure, white_balance, product_photography]":
        raise ValueError("quality anchor must not control yarn geometry")


def validate_lock(lock_path: Path) -> None:
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    roles = [attachment.get("role", "") for attachment in lock.get("reference_attachments", [])]
    expected = ["design_source_pattern_and_colour_authority", "detail_camera_only", "accepted_quality_anchor", "construction_only"]
    if roles != expected:
        raise ValueError(f"final-quality lock requires ordered roles {expected}, got {roles}")
    if lock.get("detail_camera_control") != "declared_real_camera_anchor":
        raise ValueError("final-quality lock must record the declared real camera anchor")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lock", type=Path)
    parser.add_argument("--design", type=Path, help="report whether an exact-paired packet applies")
    args = parser.parse_args()
    validate_manifest()
    if args.lock:
        validate_lock(args.lock)
    route = "unmatched_default"
    if args.design:
        source_hash = hashlib.sha256(args.design.read_bytes()).hexdigest()
        route = "sample_02_exact_paired" if source_hash == "8cf1cad996defe75a0061aa879ed21080d79ec936cbf51ddf06460a25f71c4a3" else route
    print(json.dumps({"status": "pass", "manifest": str(MANIFEST), "lock_checked": bool(args.lock), "route": route}))


if __name__ == "__main__":
    main()
