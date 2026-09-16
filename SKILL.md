---
name: carpet-visualizer
description: Generate exact-topology carpet visual samples from supplied artwork with a genuinely yarn-built surface; use for rug concept review and material screening, not manufacturing approval. Reject flat artwork with a texture or luminance overlay.
---

# Carpet Visualizer

Turn one carpet design into two coordinated visual samples: a material close-up and a full-product overview. Pattern geometry is a hard data contract; physical construction may change, artwork topology may not.

## Input contract

Require a legible `design_source`. Accept an optional material selection, detail corner, explicit colour card, task-specific references, paired mapping example, or scene-style reference.

If the user supplies only artwork, read [material library](references/material-library.md) and select the library entry marked `default_for_design_only: true`. Do not ask for a construction when a valid default exists. Supported construction slugs are `printed-low-pile`, `flatwoven`, `wilton-flatweave`, `loop-pile`, and `cut-pile`.

Classify every input before generation:

- `design_source`: owns the current rug outline, motifs, adjacency, symmetry, negative space, and default colours.
- `colour_card`: overrides only explicitly mapped current colour regions.
- `construction_reference`: owns physical structure only; use its declared `macro_detail`, `product_scale_crop`, or `overall_product` sub-role.
- `paired_mapping_example`: an exact historical trio of design, corresponding product overview, and corresponding material detail; teaches design-to-physical translation only.
- `scene_style_reference`: controls camera, light, background, crop, and presentation only.
- `quality_anchor`: indicates an accepted polish level only and is weaker than real construction evidence.

Resolve `detail_corner` in the upright `design_source` coordinate frame. Accept `upper_left`, `upper_right`, `lower_left`, or `lower_right`; use `lower_left` when the user does not choose one. Keep that orientation in both outputs without mirroring or rotating the rug. The detail must show the selected corner junction, both adjacent exterior edges with their binding, and enough adjacent border motif and colour boundary to locate the crop in the overview. Before generation, build `design_detail_crop` only as a source-coordinate inspection aid; do not attach a cropped or perspective-warped artwork as a detail reference. Attach the complete current `design_source` and use the declared camera-angle anchor to select the detail framing. This preserves every original perimeter-to-pattern spacing while the upper frame continues through the same rug plane. Run [the deterministic control builder](scripts/prepare_design_controls.py) when the input is a local raster.

The current `design_source` is the sole current-pattern authority. Material, paired, style, and quality references must not contribute motifs or current colours. Colour authority order is explicit mapped colour card, then current design source. Read [exact topology lock](references/topology-lock.md) before generation; it defines the default `topology_mode: exact`, proof requirements, and fail-closed backend decisions.

Inspect every image used. Never infer a named fibre, yarn composition, density, colour code, named loom process, or manufacturing setting. Read [material profiles](references/material-profiles.md) for the selected construction and [material config schema](references/material-config-schema.md) when editing a reusable entry. When a material manifest declares a rendering branch, read that branch before prompting. For `wilton-flatweave-01`, always use [the Wilton flatweave branch](references/wilton-flatweave-branch.md).

## Resolve material evidence

For a bundled material, open its `manifest.yaml`, verify every referenced asset exists, and inspect the declared generation inputs before prompting. When the manifest declares paired mappings, read [paired mapping calibration](references/paired-mapping-calibration.md) and run `python scripts/validate_paired_mappings.py` before use. Prefer neutral derived construction images when the manifest provides them; retain originals as audit and visual-inspection evidence.

Set `reference_strength` to:

- `task_reference_grounded` when usable task-specific real material photos are supplied;
- `library_grounded` when bundled real material references are used;
- `profile_only` when a generic profile is the only evidence.

Use a paired mapping example only when all three images are present and declared as an exact match. An unpaired product or detail photo remains a construction or style reference. Missing paired examples do not block generation.

When `render_branch: wilton_flatweave` is selected, keep the current design as the sole pattern and colour authority. Attach the complete design, a generic real camera-and-construction anchor from a different design, and the multi-unit micro construction anchor in that order. Paired mappings are calibration evidence only: their overview and detail files must never be attached when their design hash matches the current source. A quality anchor is optional and may control only exposure, white balance, and general product-photo finish; it must never control yarn geometry or camera geometry. The micro anchor validates local yarn-unit geometry, exposed cross yarn, and gap proportion; the grammar tile remains audit evidence for lane staggering and open channels. No secondary reference can provide current motifs, layout, or colours.

## Surface construction contract

For `wilton-flatweave`, the visible rug must be built from one shared low-relief woven system across the ground, motifs, boundaries, and perimeter. Reconstruct short and longer multi-filament yarn bundles in product-directional lanes. Keep a clearly visible, staggered pattern of bundle ends and open shadowed longitudinal channels where finer interlacing threads remain exposed; do not turn those lanes into an equal-pitch grid. The user confirms the Wilton flatweave classification; the evidence still does not establish a named fibre, density, or loom setting. Colour changes happen inside this same system. The `design_source` is an invisible structure-and-colour map for this stage, not a finished RGB surface to display.

Require `surface_build_mode: yarn_geometry_or_weave_synthesis`. A pipeline that displays the source artwork and then applies grayscale, luminance, normal, emboss, displacement, noise, or generic texture over it is `surface_build_mode: overlay` and fails the Wilton flatweave material gate. Do not call overlay output a woven carpet sample, even when the pattern proof passes.

Before accepting `material_detail`, inspect at 100% an equal-scale plain-field crop and a patterned-boundary crop. Both crops must show the same multi-filament yarn units, binding tracks, coarse low-relief dimensionality, and fibre response. The close detail camera must be raking and oblique enough for the near corner to sit forward of the receding plane, with visibly larger near bundles and shallow side shadows. A smooth colour field, a printed-looking motif edge, a separate raised motif layer, a near-vertical flattened camera, or a different yarn family in either crop is an immediate `pattern_material_mismatch` failure and stops `product_overview`.

## Build the render lock

Create a compact render lock before generation. Copy only supported observations into `construction_lock` across these material axes: construction, upright-product orientation, yarn geometry, organisation/interlacing, scale behaviour, relief, finish/light response, boundary behaviour, and edge geometry. Prefer physical descriptions over aesthetic adjectives. Task-specific evidence overrides the bundled library, which overrides a generic profile. Mark profile-only output as provisional.

Express every directional construction observation in upright `design_source` coordinates. When a reference is folded, sideways, mirrored or rotated, use its declared orientation notes to normalise the coarse raised-yarn, fine cross-yarn and fine ground-anchor axes; do not copy raw image-axis direction into the output.

Include the selected material's `anti_substitutions` in the lock. Use them as a rejection check for visible material identity, not as additional visual inspiration.

Lock the current design topology in source coordinates: retain the rug outline, every motif instance and repeat order, principal boundaries, junction connectivity, containment and adjacency, symmetry, negative space, and mapped colours. Camera perspective may apply only the declared transform. Any redraw, merge, split, omission, invention, mirror, reorder, or unexplained displacement fails the lock. “Looks similar” and “recognisable” are never pass evidence.

## Choose the rendering backend

Read [capabilities](CAPABILITIES.md), [backend strategies](references/backend-strategies.md), and [exact topology lock](references/topology-lock.md) before choosing a rendering backend. Use one of two explicit routes. The default for a user-facing Wilton visual sample is the **reference-grounded visual route**: attach complete design, a generic camera-and-construction anchor from a different design, and a generic multi-unit micro construction anchor. Record `topology_mode: approximate`. The **exact-proof route** creates only an aligned structure proof and anchor report; it is not a texture renderer. Reference-image input alone never upgrades an approximate visual to exact. Record the actual backend, reference paths and roles, topology mode, proof path, and `surface_build_mode` in the render lock.

When no image-generation backend is available, prepare the complete prompt packet, render lock, reference-role list, and delivery checklist for external execution. Label this result `external_execution_required`; do not claim images were generated.

For the reference-grounded visual route, read [the Wilton flatweave branch](references/wilton-flatweave-branch.md). Attach current design, declared generic camera-and-construction anchor, and declared generic multi-unit micro construction anchor. Label the result `topology_mode: approximate`. Do not generate a product overview until the user accepts the material detail. `task_reference_grounded` is allowed only when the recorded generation request actually attached the real construction image; otherwise use `library_grounded` or `profile_only`.

For runtime-specific setup, read [Codex adapter](adapters/codex.md) in Codex or [generic-agent adapter](adapters/generic-agent.md) in another agent environment.

## Generate the pair

Use a strict, fail-closed detail gate:

1. Run [the deterministic control builder](scripts/prepare_design_controls.py), keep the source SHA-256, and create the source-coordinate anchor register. A user-facing reference-grounded visual uses `topology_mode: approximate`; reserve `exact` for an actual controllable structure-and-material backend.
2. Select one branch. When the material declares `render_branch: wilton_flatweave`, read only [the Wilton flatweave branch](references/wilton-flatweave-branch.md) for generation and gating. Otherwise read [prompt templates](references/prompt-templates.md).
3. Choose the backend before spending a generation call. For an exact proof, run `python scripts/render_wilton_calibrated.py <design_source> <out_dir>` only to create `structure_proof.png` and a proof-only lock. It must never create `material_detail` or `product_overview`. If the user requests an exact final textile render but no independently controllable material backend exists, return `external_execution_required`.
4. For the user-facing visual route, attach the complete current design, declared generic camera-and-relief anchor, and generic multi-unit micro construction anchor. The complete design owns all outline, binding, inner lock line, motif, spacing, and colour relationships. The current design's paired overview and detail are forbidden references, even when a hash match exists. Real references control only physical rendering and camera; the optional quality anchor controls only exposure, white balance, and overall product-photo finish. Record every actual attachment in the lock. Do not substitute the local proof renderer for this step.
5. Inspect the material detail at 100% against the camera-angle anchor, an equal-scale real macro, and the full current design. Require the same bundle direction, visibly open longitudinal channels, adjacent-lane staggering, short-and-long unit variation, non-uniform filament response, fine interlacing, coarse raised middles, shallow side shadows, wrapped edge, visible multi-filaments, full midsections, and tapering ends. Confirm the camera follows the declared anchor: the near selected corner is foreground, one bound edge recedes upward, the far field continues through the upper frame, and original design spacing stays intact. Reject a uniform rounded-rectangle grid, continuous ribbing, closed equal-pitch lattice, smooth fill, RGB texture overlay, construction-reference pattern leakage, altered perimeter-to-pattern spacing, or a cut-off far rug edge. The user accepts or rejects this approximate visual detail.
6. Only after accepted detail review, generate `product_overview` from the full current design and declared generic construction references. Keep the same construction family, bundle direction, relief, colour mapping, edge treatment, and light direction. Label the overview `topology_mode: approximate`; it is a visual sample, not proof of exact topology.

For a controllable local backend, send current-design region and edge controls only to the structure branch, construction references only to the material branch, and repairs only through masks. Preserve the seed and all independent control values.

Use a flat-laid product-record presentation by default: a neutral dark textile ground, near-overhead view, mild near-to-far perspective, and no furnishings. Keep exposure clear enough to inspect weave shadows, colour separation, wrapped edges, and low-relief highlights without flattening the construction.

## Lightweight quality gate

Read [quality rubric](references/quality-rubric.md) and inspect each output when generated. In exact mode, `pattern_gate: pass` requires a passing aligned structure-proof command plus a completed anchor register; visual impression alone cannot pass it. The material-detail review must include the 100% plain-field/pattern-boundary comparison from the surface construction contract, the declared camera-anchor framing comparison, and a pattern-perimeter registration check. Record `pass`, `caveat`, or `fail` for topology, material, construction orientation, pattern-ground parity, detail localisation, detail texture view, pattern-perimeter registration, overview framing, presentation tone, relief and lustre, cross-scale consistency, colour authority, and edge finish, plus the applicable failure tags. Any `fail` or `unknown` stops the sequence. Do not regenerate automatically; report the failed category and let the user request one targeted retry.

## Deliver

When the pair passes, return:

- one `material_detail` image;
- one `product_overview` image;
- material ID, construction, selected detail corner, reference strength, mapping mode, colour authority, edge finish, render lock, and evaluation record;
- topology mode, topology-control capability, source hash, structure-proof path, verifier command/result, and anchor register;
- the final prompts;
- visible fidelity caveats.

When the detail is rejected, return only the failed detail when it is useful for diagnosis, its gate record, the final detail prompt, and the reason overview generation stopped.

In Chinese-facing prompts, labels, and delivery text, call the visible surface quality `肌理`, not `材质`. Keep stable internal identifiers such as `material_id` and `material_detail` unchanged for compatibility.

For `external_execution_required`, return the same render metadata, the final prompts, the ordered reference attachments, and a checklist for inspecting the two required outputs after they are generated.

End with: “Visual sample only — confirm colour, yarn, pile, density, and construction with physical sampling.”

When evaluating a new or changed material entry, read [test cases](references/test-cases.md) and run the smallest case that exercises the change.
