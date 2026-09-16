"""Extract the real local weave grammar tile used by the Wilton visual route."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
ASSET_ROOT = ROOT / "assets" / "material-library" / "wilton-flatweave-01"
SOURCE = ASSET_ROOT / "construction" / "sample-03-detail-b.jpg"
OUTPUT = ASSET_ROOT / "derived" / "wilton-open-channel-grammar-tile-v1.png"

# This window deliberately excludes the binding and any recognisable motif.
# The source was photographed sideways; rotate it into upright product coordinates.
# It retains multiple bundle lanes, open channels, cross yarns, and staggered ends.
CROP = (2350, 1100, 4450, 3300)
ROTATE_DEGREES = 90


def main() -> None:
    with Image.open(SOURCE) as source:
        if source.size != (5712, 4284):
            raise ValueError(f"unexpected source dimensions: {source.size}")
        tile = source.crop(CROP).convert("RGB").rotate(ROTATE_DEGREES, expand=True)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    tile.save(OUTPUT, "PNG", optimize=True)
    print(
        json.dumps(
            {
                "source": str(SOURCE),
                "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                "crop": CROP,
                "rotate_degrees": ROTATE_DEGREES,
                "output": str(OUTPUT),
                "output_sha256": hashlib.sha256(OUTPUT.read_bytes()).hexdigest(),
                "size": tile.size,
            }
        )
    )


if __name__ == "__main__":
    main()
