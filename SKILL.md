---
name: carpet-visualizer
description: Generate a carpet product overview and material close-up from supplied artwork, using selectable bundled or task-specific material references. Use for rug concept review and material screening, not manufacturing approval.
---

# Carpet Visualizer

Turn one carpet design into two coordinated visual samples: a material close-up and a full-product overview. Preserve the design topology while applying a selected physical construction.

## Input contract

Require a legible `design_source`. Accept an optional material selection, detail corner, explicit colour card, task-specific references, paired mapping example, or scene-style reference.

If the user supplies only artwork, read [material library](references/material-library.md) and select the library entry marked `default_for_design_only: true`. Do not ask for a construction when a valid default exists. Supported construction slugs are `printed-low-pile`, `flatwoven`, `jacquard`, `loop-pile`, and `cut-pile`.

Classify every input before generation:

- `design_source`: owns the current rug outline, motifs, adjacency, symmetry, negative space, and default colours.
- `colour_card`: overrides only explicitly mapped current colour regions.
- `construction_reference`: owns physical structure only; use its declared `macro_detail`, `product_scale_crop`, or `overall_product` sub-role.
- `paired_mapping_example`: an exact historical trio of design, corresponding product overview, and corresponding material detail; teaches design-to-physical translation only.
- `scene_style_reference`: controls camera, light, background, crop, and presentation only.
- `quality_anchor`: indicates an accepted polish level only and is weaker than real construction evidence.

Resolve `detail_corner` in the upright `design_source` coordinate frame. Accept `upper_left`, `upper_right`, `lower_left`, or `lower_right`; use `lower_left` when the user does not choose one. Keep that orientation in both outputs without mirroring or rotating the rug. The detail must show the selected corner junction, both adjacent exterior edges with their binding, and enough adjacent border motif and colour boundary to locate the crop in the overview.

The current `design_source` is the sole current-pattern authority. Material, paired, style, and quality references must not contribute motifs or current colours. Colour authority order is explicit mapped colour card, then current design source.

Inspect every image used. Never infer a named fibre, pile height, density, colour code, or manufacturing process. Read [material profiles](references/material-profiles.md) for the selected construction and [material config schema](references/material-config-schema.md) when editing a reusable entry. When a material manifest declares a rendering branch, read that branch before prompting. For `jacquard-01`, use [the standard-reference branch](references/jacquard-standard-reference-branch.md) when `render_branch: standard_reference_jacquard` is selected; otherwise read the durable [jacquard detail target](references/jacquard-detail-target.md) before generating a detail.

## Resolve material evidence

For a bundled material, open its `manifest.yaml`, verify every referenced asset exists, and inspect the generation inputs before prompting. Prefer neutral derived construction images as generation inputs to reduce colour leakage; retain originals as audit and visual-inspection evidence. Neutralisation limits reference-colour leakage only; it is not a target for final exposure, saturation, contrast or scene grading.

Set `reference_strength` to:

- `task_reference_grounded` when usable task-specific real material photos are supplied;
- `library_grounded` when bundled real material references are used;
- `profile_only` when a generic profile is the only evidence.

Use a paired mapping example only when all three images are present and declared as an exact match. An unpaired product or detail photo remains a construction or style reference. Missing paired examples do not block generation.

When `render_branch: standard_reference_jacquard` is selected, the declared standard texture references are the primary construction inputs. Keep the original construction photos for audit only and do not attach them alongside the standard packet.

## Build the render lock

Create a compact render lock before generation. Copy only supported observations into `construction_lock` across these material axes: construction, upright-product orientation, yarn geometry, organisation/interlacing, scale behaviour, relief, finish/light response, boundary behaviour, and edge geometry. Prefer physical descriptions over aesthetic adjectives. Task-specific evidence overrides the bundled library, which overrides a generic profile. Mark profile-only output as provisional.

Express every directional construction observation in upright `design_source` coordinates. When a reference is folded, sideways, mirrored or rotated, use its declared orientation notes to normalise the coarse raised-yarn, fine cross-yarn and fine ground-anchor axes; do not copy raw image-axis direction into the output.

Include the selected material's `anti_substitutions` in the lock. Use them as a rejection check for visible material identity, not as additional visual inspiration.

Lock the current design topology: retain the rug outline, motif count, principal boundaries, containment and adjacency relationships, symmetry, and negative space. Permit only local fibre-scale softening or slight irregularity. Large redraws, merged motifs, crossed or broken lines, invented regions, and historical paired-example motifs fail the lock.

## Choose the rendering backend

Read [capabilities](CAPABILITIES.md) and [backend strategies](references/backend-strategies.md) before choosing a rendering backend. Prefer an image-editing backend that accepts the current design and construction references. When the runtime supports only image generation, attach the design source and state its authority in the prompt. Record the backend name, strategy, capabilities actually used, reference budget, sequence, and any independent control values in the render lock.

When no image-generation backend is available, prepare the complete prompt packet, render lock, reference-role list, and delivery checklist for external execution. Label this result `external_execution_required`; do not claim images were generated.

For runtime-specific setup, read [Codex adapter](adapters/codex.md) in Codex or [generic-agent adapter](adapters/generic-agent.md) in another agent environment.

## Generate both outputs

Read [prompt templates](references/prompt-templates.md) for the legacy path, then use the selected backend in edit/reference mode. Generate both outputs without waiting for user approval.

If the selected material declares `render_branch: standard_reference_jacquard`, read [the standard-reference branch](references/jacquard-standard-reference-branch.md) and follow its reference packet, prompt skeleton, presentation keywords, and acceptance gate. That branch supersedes the legacy jacquard detail target and the quantitative jacquard construction passages below for this run; keep the current design source as the only pattern and colour authority.

For a preview-only backend outside `standard_reference_jacquard`, use no more than three supporting references in addition to the design source: normally neutral macro detail, neutral product-scale crop, and overall edge evidence only when needed. When no task-specific photography setup is explicitly requested, the durable detail target supplies the camera and presentation; the ordered generation packet contains only the current design and selected construction references. Do not infer or attach images from earlier conversation turns. Generate in this order:

1. Generate a close contextual material detail of `detail_corner`. Apply the durable jacquard detail target: an ultra-close product macro from a low grazing diagonal viewpoint, with the camera 8–12 degrees above the rug plane and the lens nearly level with and just above the near binding. Make the near binding side face prominent, the near crowns visibly larger than distant crowns, and the surface recede strongly through foreshortening. Let the rug surface occupy about 96–98% of the frame. Retain the complete near corner junction, short segments of both adjoining edges, and only enough nearby border artwork to locate the crop. Use bright high-key grazing light, crisp fibre-scale self-shadowing, luminous strand highlights, and sufficient depth of field to keep near and central interlacing sharp while the far field softens gently. The detail target is self-contained; use a scene-style image only when the user explicitly supplies one for this run.
2. Inspect the detail before using it as an anchor. Camera passes only when the near binding side face is prominent and the near-to-far scale change, surface recession and focus falloff match a genuinely low grazing macro view. For `jacquard-01`, mentally rectify perspective into upright rug coordinates: vertical raised crowns remain dominant but expose a continuous horizontal fine-yarn rhythm through plain areas, motifs and colour boundaries. The vertical crowns use two related scales, with larger dominant crowns and smaller secondary crowns naturally interleaved. As a visual exposure target, coarse vertical crowns occupy about 55–65% of the woven surface, clearly exposed fine horizontal yarns about 25–35%, and recessed vertical ground threads the remaining channels. Relief passes only when soft twisted strands bend over, compress against and sink between the finer yarn systems with small natural variation. Treat every diagonal or stepped artwork line as a colour-region transition inside the same weave: it may gain local relief from greater crown exposure, but the same short coarse crowns stay vertical, horizontal fine yarns remain visible across the line, and no single smooth contour tube or independent piping/embroidery layer is introduced. Use the detail as `material_detail_anchor` only when the corner, camera, direction, yarn balance, relief, and pattern-line treatment all pass. Otherwise omit it from overview references, record the failed categories, and report the failure.
3. Generate the overview from the current design, render lock, usable detail anchor, and only the scale, binding, paired-mapping, or style references needed. Use a directly overhead, level view with the rug plane parallel to the image plane, its long edges parallel to the frame, and no oblique perspective. Match the canvas to the rug aspect ratio where possible; keep the complete bound outline visible while filling about 90–95% of the frame with a narrow, even background margin. Preserve the upright design orientation so `detail_corner` maps to the same visible corner. The product-scale reference, not the detail anchor, owns visible texture scale. At product distance, reduce the apparent size of individual yarn or pile elements while retaining the construction's supported tactile hierarchy and relief instead of smoothing it away.

Inspect equal-scale areas from a plain field and a patterned boundary. They must share one yarn family, a two-scale vertical crown hierarchy, fine-yarn spacing, three-system interlacing logic, directional rhythm and finish. For `jacquard-01`, coarse raised yarns run vertically and dominate without closing the surface; finer cross yarns remain continuously visible horizontally through both pattern and ground; fine recessed ground or anchoring yarns also run vertically. All three inherit the local design-source colour. Pattern-driven exposure may vary locally, but motif edges must preserve the horizontal fine-yarn share and the same interlacing as the plain field.

For a controllable local backend, keep topology and material on separate branches: region/edge controls own structure, a reference or IP-Adapter branch owns material, and a mask owns local repair. For strict cross-scale consistency, first generate and approve the overview structure, then derive the detail from that result by crop and local inpainting. Preserve the seed and all independent control values.

The detail and overview must express the same construction, yarn hierarchy, relief distribution, colour mapping, edge treatment, and light direction. When the backend creates separate images, require visual consistency rather than literal pixel continuity.

Use a bright commercial-product presentation by default. Keep exposure high and clean, whites luminous, colours clear, and tonal separation crisp with medium-high contrast. Preserve useful weave shadows and highlight detail without a grey veil, muddy low saturation, underexposure, flat subdued grading, clipped highlights, or crushed shadows. Physical finish still follows the construction lock; presentation brightness must not flatten the relief or turn fibre highlights into plastic gloss.

## Lightweight quality gate

Read [quality rubric](references/quality-rubric.md) and inspect both outputs once. Record `pass`, `caveat`, or `fail` for topology, material, construction orientation, pattern-ground parity, detail localisation, detail texture view, overview framing, presentation tone, cross-scale consistency, colour authority, and edge finish, plus the applicable failure tags. Do not regenerate automatically. Report concrete caveats and let the user request one targeted retry that changes only the failed category.

## Deliver

When images are generated, return:

- one `material_detail` image;
- one `product_overview` image;
- material ID, construction, selected detail corner, reference strength, mapping mode, colour authority, edge finish, render lock, and evaluation record;
- the final prompts;
- visible fidelity caveats.

In Chinese-facing prompts, labels, and delivery text, call the visible surface quality `肌理`, not `材质`. Keep stable internal identifiers such as `material_id` and `material_detail` unchanged for compatibility.

For `external_execution_required`, return the same render metadata, the final prompts, the ordered reference attachments, and a checklist for inspecting the two required outputs after they are generated.

End with: “Visual sample only — confirm colour, yarn, pile, density, and construction with physical sampling.”

When evaluating a new or changed material entry, read [test cases](references/test-cases.md) and run the smallest case that exercises the change.
