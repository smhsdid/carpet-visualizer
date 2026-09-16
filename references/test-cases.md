# Carpet visualizer test cases

Run the smallest case exercising the changed behaviour.

## Case 1: design-only default

Input: one legible upright artwork.

Expected: `wilton-flatweave-01` is selected; exact mode prepares controls and proof; an unmatched detail uses complete current design first, declared real detail-camera anchor second, and multi-unit micro construction anchor third; overview waits for all detail gates.

## Case 2: reference inventory

Input: bundled manifest.

Expected: all ten real source images resolve; its detail and overview references resolve; no AI artwork appears in `audit_references`; the Wilton flatweave classification is explicitly user-confirmed; no fibre, density, loom setting, or pile-specification claim exists.

## Case 3: surface identity

Input: equal-scale pattern and ground crops.

Expected: both contain product-directional lanes of visibly short and longer multi-filament bundles, offset ends across adjacent lanes, open shadowed longitudinal channels exposing finer interlacing, low crowns, shallow gaps, and the same restrained finish. Smooth fill, bead grid, closed equal-pitch lattice, basket weave, rope, deep pile, or an independently raised motif fails.

## Case 4: edge and orientation

Input: a lower-left detail crop.

Expected: rounded wrapped binding, inner locking line, complete foreground corner, both edges, roughly 30-degree raking plane recession, visibly larger near bundles, and construction-wide row direction survive. The perspective control keeps outline, binding, lock line, and interior artwork registered on one continuous plane; the upper frame remains carpet surface rather than a false far edge. Texture may not turn along the motif.

## Case 5: exact topology and overlay regression

Input: artwork, an aligned source proof, and an RGB-plus-texture detail.

Expected: source proof validates; RGB-plus-texture detail is `overlay`, fails the surface gate, and stops the overview. A preview-only exact backend returns `external_execution_required` rather than claiming a pass.

## Case 6: paired mapping calibration

Input: `wilton-flatweave-01/paired-mappings.json`.

Expected: each of the three pairs has an existing `design`, `overview`, and `detail` whose SHA-256 matches its manifest record. Excluding one pair reports the remaining two as the calibration set. The current design remains the sole authority for a new render's pattern and colours.

## Case 7: proof renderer cannot deliver final texture

Input: `scripts/render_wilton_calibrated.py` with an artwork and a temporary output directory.

Expected: it writes only `structure_proof.png`, controls, and a proof-only render lock. The lock has `reference_strength: none`, `material_detail: null`, and `product_overview: null`. A user-facing unmatched Wilton visual instead requires a recorded design reference, real camera anchor, and the declared multi-unit micro construction anchor.

## Case 8: paired-reference leakage regression

Input: `wilton-flatweave-01/manifest.yaml` and the sample-02 design.

Expected: a SHA-256 match does not change the generic packet. The detail packet orders complete current design, sample-01 generic camera-and-construction anchor, then generic micro construction anchor. The sample-02 overview and material detail are forbidden generation inputs.

## Case 9: camera-anchor framing and spacing regression

Input: a complete design source and the declared lower-left detail camera anchor.

Expected: the complete source remains the only geometry authority while the real anchor sets low-raking corner framing. The upper frame continues through rug surface, the left bound edge recedes as in the anchor, and outline-to-pattern spacing remains unchanged. A generated detail with expanded perimeter gap, pattern drift, or a false top edge fails `camera_pattern_registration_mismatch` and stops overview generation.
