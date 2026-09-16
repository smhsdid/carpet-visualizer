# Carpet visualizer test cases

Run the smallest case exercising the changed behaviour.

## Case 1: design-only unified flow

Input: one legible upright artwork.

Expected: `wilton-flatweave-01` is selected; the fixed lower-left controls are prepared; the complete design is attached first, followed by the declared camera/construction and micro construction references; a detail is generated, lightly checked, and the overview is generated automatically without asking for confirmation.

## Case 2: reference inventory

Input: bundled manifest.

Expected: all ten real source images resolve; its detail and overview references resolve; no AI artwork appears in `audit_references`; no fibre, density, loom setting, or pile-specification claim exists; the default run strength is `library_grounded`.

## Case 3: surface identity

Input: equal-scale pattern and ground crops.

Expected: both contain product-directional lanes of visibly short and longer multi-filament bundles, offset ends across adjacent lanes, open shadowed longitudinal channels exposing finer interlacing, low crowns, shallow gaps, and the same restrained finish. Smooth fill, bead grid, closed equal-pitch lattice, basket weave, rope, deep pile, or an independently raised motif fails the check.

## Case 4: fixed lower-left edge and orientation

Input: a complete design source.

Expected: the generated detail shows the lower-left corner, both adjacent bound edges, roughly raking plane recession, visibly larger near bundles, construction-wide row direction, and continuous rug surface through the upper frame. No corner parameter is required or accepted.

## Case 5: surface overlay regression

Input: artwork and an RGB-plus-texture detail.

Expected: the detail is recorded as `surface_build_mode: overlay`, receives a material caveat or failure tag, and the overview still follows the unified flow unless the output is technically invalid. The final record retains the prompt and parameters that produced the output.

## Case 6: paired mapping calibration

Input: `wilton-flatweave-01/paired-mappings.json`.

Expected: each of the three pairs has an existing `design`, `overview`, and `detail` whose SHA-256 matches its manifest record. The current design remains the sole authority for a new render's pattern and colours.

## Case 7: diagnostic helper cannot deliver the final pair

Input: `scripts/render_wilton_calibrated.py` with an artwork and a temporary output directory.

Expected: it writes only diagnostic structure evidence and a diagnostic record. It never presents those files as `material_detail` or `product_overview`.

## Case 8: paired-reference leakage regression

Input: each paired design in turn.

Expected: the attachment selector checks the current design SHA-256 and never selects the matching pair's overview or detail. A non-matching generic camera anchor and the micro construction anchor are selected instead.

## Case 9: prompt and parameter persistence

Input: one complete design source and a successful generation.

Expected: the run record contains the final detail prompt, final overview prompt, effective parameters, seed or replay data when available, source hash, ordered reference paths and hashes, output paths, and lightweight check results.

## Case 10: automatic sequence

Input: a generated detail that contains visual caveats but opens successfully.

Expected: the caveats are recorded and the overview is generated automatically. A missing, unreadable, or technically invalid detail is the only condition that stops the sequence.
