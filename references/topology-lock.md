# Pattern fidelity rules

Pattern fidelity is a data-integrity requirement, not a style preference. The current `design_source` is the literal source of the rug's structure. Words such as “similar”, “recognisable”, “inspired by”, or “preserve generally” are not evidence that the pattern was preserved.

## Unified preservation target

Every run uses the same strict preservation target. Preserve, in the source coordinate frame, the silhouette, principal boundaries, every motif instance and repeat order, junction connectivity, containment, negative-space components, symmetry, and mapped colour region. The camera may change the presentation, but it must not intentionally redraw, merge, split, invent, omit, mirror, reorder, or independently re-space visible artwork.

The target applies to every artwork without a complexity branch. When the image backend introduces visual drift, record it in the evaluation record as a caveat and retain the original source hash.

## Deterministic preflight

For a local raster, run:

```text
python scripts/prepare_design_controls.py <design_source> <control_dir>
```

The helper always uses the fixed lower-left detail area. Keep the original source, its SHA-256, and the generated `design_lock.json`. The control directory contains the source-coordinate detail crop, pattern-region information, and full/detail edge maps. These files are structural controls and audit evidence; construction references never replace them.

Before prompting, create an anchor register from the source and its controls. At minimum enumerate the outer outline, the lower-left corner junction, each visible repeat in the detail crop, the inner boundary, enclosed field, and every colour transition. Record source-coordinate positions and adjacency.

## Diagnostic proof

A deterministic structure snapshot or proof can be produced for troubleshooting and comparison. It must be clearly labelled as diagnostic evidence, not as a material-detail or product-overview image. It does not replace the visual generation call and is not required before generating the pair.

The topology validator compares coarse region labels and boundaries. It is useful for regression detection, but it is not a manufacturing certification and cannot prove that a semantic image backend preserved every pixel or motif.

## Prompt contract

Prompts must say that the current artwork is the literal structure target, that construction references control only the physical surface, and that the artwork is copied through the declared camera presentation. Prompt wording cannot turn a visibly changed pattern into a pass.
