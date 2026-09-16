# Carpet visualizer test cases

Run the smallest case exercising the changed behaviour.

## Case 1: design-only default

Input: one legible upright artwork.

Expected: `wilton-flatweave-01` is selected; exact mode prepares controls and proof; detail uses the crop first and one declared real reference second; overview waits for all detail gates.

## Case 2: reference inventory

Input: bundled manifest.

Expected: all ten real source images resolve; its detail and overview references resolve; no AI artwork appears in `audit_references`; the Wilton flatweave classification is explicitly user-confirmed; no fibre, density, loom setting, or pile-specification claim exists.

## Case 3: surface identity

Input: equal-scale pattern and ground crops.

Expected: both contain stable long-axis rows of short multi-filament bundles, finer interlacing threads, low crowns, shallow gaps, and the same restrained finish. Smooth fill, bead grid, basket weave, rope, deep pile, or an independently raised motif fails.

## Case 4: edge and orientation

Input: a lower-left detail crop.

Expected: rounded wrapped binding, inner locking line, complete corner, both edges, and construction-wide row direction survive. Texture may not turn along the motif.

## Case 5: exact topology and overlay regression

Input: artwork, an aligned source proof, and an RGB-plus-texture detail.

Expected: source proof validates; RGB-plus-texture detail is `overlay`, fails the surface gate, and stops the overview. A preview-only exact backend returns `external_execution_required` rather than claiming a pass.
