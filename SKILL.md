---
name: carpet-visualizer
description: Generate a realistic carpet product overview and material close-up from supplied artwork, using selectable bundled or task-specific material references. Use for rug concept review and material screening, not manufacturing approval.
---

# Carpet Visualizer

Turn one carpet design into two coordinated visual samples: a material close-up and a full-product overview. Preserve the design topology while applying a selected physical construction.

## Input contract

Require a legible `design_source`. Accept an optional material selection, explicit colour card, task-specific references, paired mapping example, or scene-style reference.

If the user supplies only artwork, read [material library](references/material-library.md) and select the library entry marked `default_for_design_only: true`. Do not ask for a construction when a valid default exists. Supported construction slugs are `printed-low-pile`, `flatwoven`, `jacquard`, `loop-pile`, and `cut-pile`.

Classify every input before generation:

- `design_source`: owns the current rug outline, motifs, adjacency, symmetry, negative space, and default colours.
- `colour_card`: overrides only explicitly mapped current colour regions.
- `construction_reference`: owns physical structure only; use its declared `macro_detail`, `product_scale_crop`, or `overall_product` sub-role.
- `paired_mapping_example`: an exact historical trio of design, corresponding product overview, and corresponding material detail; teaches design-to-physical translation only.
- `scene_style_reference`: controls camera, light, background, crop, and presentation only.
- `quality_anchor`: indicates an accepted polish level only and is weaker than real construction evidence.

The current `design_source` is the sole current-pattern authority. Material, paired, style, and quality references must not contribute motifs or current colours. Colour authority order is explicit mapped colour card, then current design source.

Inspect every image used. Never infer a named fibre, pile height, density, colour code, or manufacturing process. Read [material profiles](references/material-profiles.md) for the selected construction and [material config schema](references/material-config-schema.md) when editing a reusable entry.

## Resolve material evidence

For a bundled material, open its `manifest.yaml`, verify every referenced asset exists, and inspect the generation inputs before prompting. Prefer neutral derived construction images as generation inputs to reduce colour leakage; retain originals as audit and visual-inspection evidence.

Set `reference_strength` to:

- `task_reference_grounded` when usable task-specific real material photos are supplied;
- `library_grounded` when bundled real material references are used;
- `profile_only` when a generic profile is the only evidence.

Use a paired mapping example only when all three images are present and declared as an exact match. An unpaired product or detail photo remains a construction or style reference. Missing paired examples do not block generation.

## Build the render lock

Create a compact render lock before generation. Copy only supported observations into `construction_lock`: surface structure, yarn geometry, interlacing, grain direction, relief, edge geometry, and finish. Task-specific evidence overrides the bundled library, which overrides a generic profile. Mark profile-only output as provisional.

Lock the current design topology: retain the rug outline, motif count, principal boundaries, containment and adjacency relationships, symmetry, and negative space. Permit only local fibre-scale softening or slight irregularity. Large redraws, merged motifs, crossed or broken lines, invented regions, and historical paired-example motifs fail the lock.

## Generate both outputs

Read [prompt templates](references/prompt-templates.md), then use the available image-generation tool in edit/reference mode. Generate both outputs without waiting for user approval:

1. Generate a close material detail around a representative artwork boundary, preferably where two colour regions meet.
2. Inspect the detail. If construction is usable, treat it as `material_detail_anchor`. If it contradicts the lock, omit it from overview references and continue from the lock and real construction references; report the failure.
3. Generate the overview from the current design, render lock, usable detail anchor, and only the scale, binding, paired-mapping, or style references needed.

The detail and overview must express the same construction, yarn hierarchy, relief distribution, colour mapping, edge treatment, and light direction. In `built_in_preview`, this means visual consistency rather than literal pixel continuity. Reserve `api_high_resolution` and `blender_local` as future backend values; do not claim they were used unless available and selected.

## Lightweight quality gate

Read [quality rubric](references/quality-rubric.md) and inspect both outputs once. Do not regenerate automatically. Report concrete caveats and let the user request a targeted retry.

## Deliver

Return:

- one `material_detail` image;
- one `product_overview` image;
- material ID, construction, reference strength, mapping mode, colour authority, edge finish, and render lock;
- the final prompts;
- visible fidelity caveats.

End with: “Visual sample only — confirm colour, yarn, pile, density, and construction with physical sampling.”

When evaluating a new or changed material entry, read [test cases](references/test-cases.md) and run the smallest case that exercises the change.
