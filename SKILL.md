---
name: carpet-visualizer
description: Generate pattern-preserving carpet visual samples from supplied artwork with a genuinely yarn-built surface; use for rug concept review and material screening, not manufacturing approval. Reject flat artwork with a texture or luminance overlay.
---

# Carpet Visualizer

Turn one carpet design into two coordinated visual samples: a material close-up and a full-product overview. Use one fixed generation flow for every design. Preserve the artwork's pattern structure as strictly as the selected image backend allows; do not branch on artwork complexity.

## Input contract

Require one legible `design_source`. Accept an optional material selection, explicit colour card, task-specific material references, paired mapping example, or scene-style reference.

If the user supplies only artwork, read [material library](references/material-library.md) and select the library entry marked `default_for_design_only: true`. Do not ask the user to choose a construction when a valid default exists. Supported construction slugs are `printed-low-pile`, `flatwoven`, `wilton-flatweave`, `loop-pile`, and `cut-pile`.

Classify every input before generation:

- `design_source`: owns the current rug outline, motifs, adjacency, symmetry, negative space, and default colours.
- `colour_card`: overrides only explicitly mapped current colour regions.
- `construction_reference`: owns physical structure only; use its declared `macro_detail`, `product_scale_crop`, or `overall_product` sub-role.
- `paired_mapping_example`: an exact historical trio of design, corresponding product overview, and corresponding material detail; teaches design-to-physical translation only.
- `scene_style_reference`: controls camera, light, background, crop, and presentation only.
- `quality_anchor`: controls photographic finish only and never yarn geometry, current motifs, or colours.

Use the fixed `lower_left` detail corner in the upright `design_source` coordinate frame. Do not ask for or expose a corner parameter. Keep that orientation in both outputs without mirroring or rotating the rug. The detail must show the selected corner junction, both adjacent exterior edges with their binding, enough adjacent border motif and colour boundary to locate the crop in the overview, and continuous rug surface through the upper frame.

Before generation, build `design_detail_crop` only as a source-coordinate inspection aid; do not attach a cropped or perspective-warped artwork as a generation reference. Attach the complete current `design_source`. Run [the deterministic control builder](scripts/prepare_design_controls.py) when the input is a local raster. Keep the source SHA-256 and the generated control files.

The current `design_source` is the sole current-pattern authority. Material, paired, style, and quality references must not contribute motifs or current colours. Colour authority order is explicit mapped colour card, then current design source. Read [pattern fidelity rules](references/topology-lock.md) before generation.

Inspect every image used. Never infer a named fibre, yarn composition, density, colour code, named loom process, or manufacturing setting. Read [material profiles](references/material-profiles.md) for the selected construction and [material config schema](references/material-config-schema.md) when editing a reusable entry. When a material manifest declares a rendering branch, read that branch before prompting. For `wilton-flatweave-01`, always use [the Wilton flatweave branch](references/wilton-flatweave-branch.md).

## Resolve material evidence

For a bundled material, open its `manifest.yaml`, verify every referenced asset exists, and inspect the declared generation inputs before prompting. When the manifest declares paired mappings, read [paired mapping calibration](references/paired-mapping-calibration.md) and run `python scripts/validate_paired_mappings.py` before use. Prefer neutral derived construction images when the manifest provides them; retain originals as audit and visual-inspection evidence.

Set `reference_strength` to:

- `task_reference_grounded` when usable task-specific real material photos are supplied in the current task;
- `library_grounded` when bundled real material references are used;
- `profile_only` when a generic profile is the only evidence.

Use a paired mapping example only when all three images are present and declared as an exact match. An unpaired product or detail photo remains a construction or style reference. Missing paired examples do not block the unified generation flow. Never attach the overview or detail from a pair whose design SHA-256 matches the current source.

For `wilton_flatweave`, attach the complete current design first, the declared generic camera-and-construction anchor second, and the generic multi-unit construction anchor third. The optional quality anchor may be attached only when the backend supports it and may control exposure, white balance, and product-photo finish only. Record every actual attachment, its role, and its SHA-256 in the generation record.

## Surface construction contract

For `wilton-flatweave`, the visible rug must be built from one shared low-relief woven system across the ground, motifs, boundaries, and perimeter. Reconstruct short and longer multi-filament yarn bundles in product-directional lanes. Keep visibly staggered bundle ends and open shadowed longitudinal channels where finer interlacing threads remain exposed; do not turn those lanes into an equal-pitch grid.

Colour changes happen inside this same yarn system. The `design_source` is an invisible structure-and-colour map for this stage, not a finished RGB surface to display.

Require `surface_build_mode: yarn_geometry_or_weave_synthesis`. A pipeline that displays the source artwork and then applies grayscale, luminance, normal, emboss, displacement, noise, or generic texture over it is `surface_build_mode: overlay` and fails the material check. Do not call overlay output a woven carpet sample, even when the pattern looks correct.

Before the lightweight detail check, inspect at 100% an equal-scale plain-field crop and a patterned-boundary crop. Both should show the same multi-filament yarn units, binding tracks, coarse low-relief dimensionality, and fibre response. Reject obvious smooth fill, printed-looking edges, a separate raised motif layer, a flattened camera, or a visibly different yarn family. Record the observation; do not wait for user confirmation.

## Unified generation flow

Read [capabilities](CAPABILITIES.md), [backend strategies](references/backend-strategies.md), and [pattern fidelity rules](references/topology-lock.md) before choosing the available image-generation backend. There is one user-facing route:

1. Run `python scripts/prepare_design_controls.py <design_source> <control_dir>` for a local raster. Use the fixed lower-left corner. Create the source hash and source-coordinate anchor register.
2. Select the material branch. For `wilton_flatweave`, read only [the Wilton flatweave branch](references/wilton-flatweave-branch.md) for generation rules.
3. Build the final detail prompt, final overview prompt, ordered reference list, and generation parameters before making a generation call. Save them to `render_lock.json` or the equivalent run record before generation.
4. Generate `material_detail` for the fixed lower-left corner. Do not ask the user to confirm the detail.
5. Run one lightweight check: output exists and opens, the selected corner and both bound edges are present, the upper frame continues through the rug plane, the yarn system is visible, and no obvious reference-pattern leakage or flat texture overlay is present. Record pass, caveat, or fail with evidence paths. Only a missing or unreadable output stops the sequence.
6. Automatically generate `product_overview` from the complete current design and the declared construction references. Keep the same construction family, bundle direction, relief, colour mapping, edge treatment, and light direction.
7. Update the run record with the actual backend, actual attachments, final prompts, effective parameters, output paths, source hash, and lightweight check results.

If no image-generation backend is available, prepare the complete prompt packet, render record, reference-role list, and delivery checklist for external execution. Label this result `external_execution_required`; do not claim images were generated. Do not use the proof helper as a final visual renderer.

Use a flat-laid product-record presentation by default: a neutral dark textile ground, near-overhead view, mild near-to-far perspective, and no furnishings. Keep exposure clear enough to inspect weave shadows, colour separation, wrapped edges, and low-relief highlights without flattening the construction.

## Lightweight quality record

Read [quality rubric](references/quality-rubric.md) and inspect each output when generated. This is a compact diagnostic check, not a user-approval gate. Record `pass`, `caveat`, or `fail` for pattern preservation, surface build, construction orientation, pattern-ground parity, detail localisation, detail texture view, pattern-perimeter registration, overview framing, presentation tone, relief and lustre, cross-scale consistency, colour authority, and edge finish, plus applicable failure tags.

Do not regenerate automatically. A visual caveat is recorded and the overview is still generated; only a missing, unreadable, or technically invalid output stops the sequence.

## Deliver

When the pair is generated, return:

- one `material_detail` image;
- one `product_overview` image;
- material ID, construction, fixed detail corner `lower_left`, reference strength, mapping mode, colour authority, edge finish, render record, and evaluation record;
- source hash and control paths;
- the final prompts actually sent to the image backend;
- the effective generation parameters, seed or replay information when available;
- ordered reference attachments with paths, roles, and hashes;
- visible fidelity caveats.

For `external_execution_required`, return the same render metadata, the final prompts, the ordered reference attachments, the effective parameters, and a checklist for inspecting the two required outputs after they are generated.

In Chinese-facing prompts, labels, and delivery text, call the visible surface quality `肌理`, not `材质`. Keep stable internal identifiers such as `material_id` and `material_detail` unchanged for compatibility.

End with: “Visual sample only — confirm colour, yarn, pile, density, and construction with physical sampling.”

When evaluating a new or changed material entry, read [test cases](references/test-cases.md) and run the smallest case that exercises the change.
