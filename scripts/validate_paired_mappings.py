#!/usr/bin/env python3
"""Verify that every declared Wilton mapping set is complete and immutable."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


DEFAULT_MANIFEST = (
    Path(__file__).resolve().parents[1]
    / "assets"
    / "material-library"
    / "wilton-flatweave-01"
    / "paired-mappings.json"
)
REQUIRED_ROLES = ("design", "overview", "detail")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument(
        "--exclude",
        metavar="PAIR_ID",
        help="report the two remaining calibration pairs for a leave-one-out review",
    )
    args = parser.parse_args()

    manifest_path = args.manifest.resolve()
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    material_root = manifest_path.parent
    problems: list[dict[str, str]] = []
    pair_ids: list[str] = []

    for pair in payload.get("pairs", []):
        pair_id = pair.get("id", "<missing-id>")
        pair_ids.append(pair_id)
        for role in REQUIRED_ROLES:
            artifact = pair.get(role)
            if not isinstance(artifact, dict):
                problems.append({"pair": pair_id, "role": role, "error": "missing declaration"})
                continue
            path = material_root / artifact.get("path", "")
            if not path.is_file():
                problems.append({"pair": pair_id, "role": role, "error": f"missing file: {path}"})
                continue
            actual = sha256(path)
            expected = artifact.get("sha256", "").lower()
            if actual != expected:
                problems.append(
                    {
                        "pair": pair_id,
                        "role": role,
                        "error": "sha256 mismatch",
                    }
                )

    if len(pair_ids) != 3:
        problems.append({"pair": "manifest", "role": "pairs", "error": "exactly three pairs are required"})
    if len(set(pair_ids)) != len(pair_ids):
        problems.append({"pair": "manifest", "role": "pairs", "error": "pair ids must be unique"})

    remaining = pair_ids
    if args.exclude:
        if args.exclude not in pair_ids:
            problems.append({"pair": args.exclude, "role": "exclude", "error": "unknown pair id"})
        else:
            remaining = [pair_id for pair_id in pair_ids if pair_id != args.exclude]
            if len(remaining) != 2:
                problems.append({"pair": args.exclude, "role": "exclude", "error": "leave-one-out needs two pairs"})

    result = {
        "status": "pass" if not problems else "fail",
        "manifest": str(manifest_path),
        "pairs": pair_ids,
        "leave_one_out": {"excluded": args.exclude, "calibration_pairs": remaining},
        "problems": problems,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
