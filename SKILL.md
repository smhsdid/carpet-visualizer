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

Resolve `detail_corner` in the upright `design_source` coordinate frame. Accept `upper_left`, `upper_right`, `lower_left`, or `lower_right`; use `lower_left` when the user does not choose one. Keep that orientation in both outputs without mirroring or rotating the rug. The detail must show the selected corner junction, both adjacent exterior edges with their binding, and enough adjacent border motif and colour boundary to locate the crop in the overview. Before generation, create a deterministic `design_detail_crop` from the current artwork in that corner; it is a pattern-only reference and must never be replaced by a guessed crop or a prior generated image. Use [the crop helper](scripts/prepare_design_crop.py) when the input is a local raster.

The current `design_source` is the sole current-pattern authority. Material, paired, style, and quality references must not contribute motifs or current colours. Colour authority order is explicit mapped colour card, then current design source. Read [exact topology lock](references/topology-lock.md) before generation; it defines the default `topology_mode: exact`, proof requirements, and fail-closed backend decisions.

Inspect every image used. Never infer a named fibre, yarn composition, density, colour code, named loom process, or manufacturing setting. Read [material profiles](references/material-profiles.md) for the selected construction and [material config schema](references/material-config-schema.md) when editing a reusable entry. When a material manifest declares a rendering branch, read that branch before prompting. For `wilton-flatweave-01`, always use [the Wilton flatweave branch](references/wilton-flatweave-branch.md).

## Resolve material evidence

For a bundled material, open its `manifest.yaml`, verify every referenced asset exists, and inspect the declared generation inputs before prompting. Prefer neutral derived construction images when the manifest provides them; retain originals as audit and visual-inspection evidence.

Set `reference_strength` to:

- `task_reference_grounded` when usable task-specific real material photos are supplied;
- `library_grounded` when bundled real material references are used;
- `profile_only` when a generic profile is the only evidence.

Use a paired mapping example only when all three images are present and declared as an exact match. An unpaired product or detail photo remains a construction or style reference. Missing paired examples do not block generation.

When `render_branch: wilton_flatweave` is selected, keep the current design as the sole pattern and colour authority, but attach the manifest-declared real detail reference as one secondary construction-and-camera reference when the backend supports two references. It has high construction priority for the observed bundle system, low relief, edge treatment, and close-oblique camera. It must never supply motif geometry, region placement, or colours. If the backend supports only one reference, attach the current design and mark the run `reference_limited`; do not claim the construction reference influenced generation.

## Surface construction contract

For `wilton-flatweave`, the visible rug must be built from one shared low-relief woven system across the ground, motifs, boundaries, and perimeter. Reconstruct regular short multi-filament yarn bundles in aligned rows, separated and held by finer interlacing threads. The user confirms the Wilton flatweave classification; the evidence still does not establish a named fibre, density, or loom setting. Colour changes happen inside this same system. The `design_source` is an invisible structure-and-colour map for this stage, not a finished RGB surface to display.

Require `surface_build_mode: yarn_geometry_or_weave_synthesis`. A pipeline that displays the source artwork and then applies grayscale, luminance, normal, emboss, displacement, noise, or generic texture over it is `surface_build_mode: overlay` and fails the Wilton flatweave material gate. Do not call overlay output a woven carpet sample, even when the pattern proof passes.

Before accepting `material_detail`, inspect at 100% an equal-scale plain-field crop and a patterned-boundary crop. Both crops must show the same multi-filament yarn units, binding tracks, low relief, and fibre response. A smooth colour field, a printed-looking motif edge, a separate raised motif layer, or a different yarn family in either crop is an immediate `pattern_material_mismatch` failure and stops `product_overview`.

## Build the render lock

Create a compact render lock before generation. Copy only supported observations into `construction_lock` across these material axes: construction, upright-product orientation, yarn geometry, organisation/interlacing, scale behaviour, relief, finish/light response, boundary behaviour, and edge geometry. Prefer physical descriptions over aesthetic adjectives. Task-specific evidence overrides the bundled library, which overrides a generic profile. Mark profile-only output as provisional.

Express every directional construction observation in upright `design_source` coordinates. When a reference is folded, sideways, mirrored or rotated, use its declared orientation notes to normalise the coarse raised-yarn, fine cross-yarn and fine ground-anchor axes; do not copy raw image-axis direction into the output.

Include the selected material's `anti_substitutions` in the lock. Use them as a rejection check for visible material identity, not as additional visual inspiration.

Lock the current design topology in source coordinates: retain the rug outline, every motif instance and repeat order, principal boundaries, junction connectivity, containment and adjacency, symmetry, negative space, and mapped colours. Camera perspective may apply only the declared transform. Any redraw, merge, split, omission, invention, mirror, reorder, or unexplained displacement fails the lock. “Looks similar” and “recognisable” are never pass evidence.

## Choose the rendering backend

Read [capabilities](CAPABILITIES.md), [backend strategies](references/backend-strategies.md), and [exact topology lock](references/topology-lock.md) before choosing a rendering backend. Prefer a deterministic compositor or controllable image-editing backend with separate structure and material controls. A deterministic compositor qualifies only when it synthesises visible coloured yarn units from the structure map; source-RGB-plus-luminance/texture overlay is not independent material conditioning. Reference-image input alone is not topology control. In exact mode, a preview-only semantic backend is unsupported: set `pattern_control: unavailable`, fail the pattern gate, and stop before generating the overview. Record the backend name, strategy, capabilities actually used, reference budget, topology mode, proof path, `surface_build_mode`, and independent control values in the render lock.

When no image-generation backend is available, prepare the complete prompt packet, render lock, reference-role list, and delivery checklist for external execution. Label this result `external_execution_required`; do not claim images were generated.

For runtime-specific setup, read [Codex adapter](adapters/codex.md) in Codex or [generic-agent adapter](adapters/generic-agent.md) in another agent environment.

## Generate the pair

Use a strict, fail-closed detail gate:

1. Set `topology_mode: exact` unless the user explicitly accepts approximation. Run [the deterministic control builder](scripts/prepare_design_controls.py), keep the source SHA-256, and create the source-coordinate anchor register.
2. Select one branch. When the material declares `render_branch: wilton_flatweave`, read only [the Wilton flatweave branch](references/wilton-flatweave-branch.md) for generation and gating. Otherwise read [prompt templates](references/prompt-templates.md).
3. Choose the backend before spending a generation call. In exact mode, continue only if the backend can produce an aligned `structure_proof` through deterministic compositing or a real structure-control branch. If it cannot, return `external_execution_required`; do not produce a falsely exact image.
4. Produce `structure_proof` in source coordinates from design controls only, then run `python scripts/validate_topology.py <design_source> <structure_proof> --aligned`. The command must exit `0`; otherwise set `anchor_status: rejected`, stop, and report `pattern_drift`. A perspective product image is never a structure proof.
5. After the proof passes, render `material_detail` from the immutable structure proof plus the declared construction references. For Wilton flatweave, attach the deterministic crop first and one declared real detail second; construction references control only physical surface, edge, and camera. Rebuild the visible surface from the shared yarn units, using the source raster only as an invisible structure-and-colour map. Do not attach any other patterned textile or prior generated image.
6. Inspect the detail against the anchor register after inverse-mapping it to source coordinates. Every anchor must be explicitly `exact`; `changed` or `unknown` fails. Pattern topology, colour placement, corner localisation, camera, integral woven material identity, and declared yarn-unit scale are hard gates. On any failure, set `anchor_status: rejected` and do not generate `product_overview`.
7. Only after the accepted detail gate, generate `product_overview` from the full structure proof/design controls plus the product-scale construction reference. Inspect the overview with the same anchor register and require the same construction, direction, relief family, colour mapping, edge treatment, and light direction.

For a controllable local backend, send current-design region and edge controls only to the structure branch, construction references only to the material branch, and repairs only through masks. Preserve the seed and all independent control values.

Use a bright commercial-product presentation by default. Keep exposure high and clean, whites luminous, colours clear, and tonal separation crisp with medium-high contrast. Preserve useful weave shadows and highlight detail without a grey veil, muddy low saturation, underexposure, flat subdued grading, clipped highlights, or crushed shadows. Physical finish still follows the construction lock; presentation brightness must not flatten the relief or turn fibre highlights into plastic gloss.

## Lightweight quality gate

Read [quality rubric](references/quality-rubric.md) and inspect each output when generated. In exact mode, `pattern_gate: pass` requires a passing aligned structure-proof command plus a completed anchor register; visual impression alone cannot pass it. The material-detail review must include the 100% plain-field/pattern-boundary comparison from the surface construction contract. Record `pass`, `caveat`, or `fail` for topology, material, construction orientation, pattern-ground parity, detail localisation, detail texture view, overview framing, presentation tone, relief and lustre, cross-scale consistency, colour authority, and edge finish, plus the applicable failure tags. Any `fail` or `unknown` stops the sequence. Do not regenerate automatically; report the failed category and let the user request one targeted retry.

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
