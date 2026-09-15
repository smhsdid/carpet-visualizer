# Prompt templates

Use concise English prompts for the image model. Replace bracketed fields with the render lock and omit absent optional blocks. The current design source is always the edit target. These are legacy templates; when a material manifest declares a rendering branch, use that branch instead. For unbranched `jacquard-01`, read [the durable jacquard detail target](jacquard-detail-target.md) before filling the corner-detail template.

## Shared authority block

```text
Image roles are strict. The current design source is the only authority for current outline, motif geometry, placement and default colours. A mapped colour card overrides only mapped colour regions. Construction references control only their declared physical traits and have no colour or motif authority. A paired historical example teaches only how artwork translates into this construction; never copy its motif, layout or palette. A scene-style reference controls only camera, lighting, background and crop. A quality anchor controls polish only.
```

## Corner material detail

```text
Use case: carpet material screening
Output: one bright, crisp commercial-product material close-up
[shared authority block]

Design orientation: upright, matching the current design source; no mirror or rotation
Construction orientation: all yarn-system directions are expressed in upright finished-rug coordinates, not raw reference-image axes
Selected detail corner: [upper_left|upper_right|lower_left|lower_right]
Default detail corner: lower_left
Material ID: [material_id]
Construction: [construction]
Reference strength: [reference_strength]
Mapping mode: [mapping_reference_mode]
Construction lock: [orientation_frame; coarse_raised_yarn_axis; fine_cross_yarn_axis; fine_ground_anchor_axis; surface_structure; yarn_geometry; interlacing; grain_direction; scale_behavior; surface_relief; yarn_exposure_balance; boundary_behavior; yarn_colour_behavior; edge_geometry; finish]
Anti-substitutions: [material-specific anti_substitutions]
Colour authority: [colour_authority]
Colour mapping: [colour_mapping or current design-source colours]

First create a deterministic `design_detail_crop` from the current design in the selected upright corner. Use it as the sole local motif and colour-placement authority. Generate `material_detail` directly from the current design, this crop and the construction references; the product overview is not yet available and must not be used as the detail source. Create an attractive professional three-quarter macro photograph: camera approximately 25–35 degrees above the rug plane, azimuth 20–35 degrees across the two adjoining edges, with the corner and one bound edge forming a diagonal leading line into depth. Keep the complete near corner junction and both binding segments visible, fill about 96–98% of the frame with rug surface, use shallow side raking light plus soft fill, keep near and central interlacing sharp, and let the far field soften gently. Inspect this output and retain it as `material_detail_anchor` only when the local pattern and construction pass.

The camera treatment is independent from material identity and is fully specified by the three-quarter macro target above. Use raking light to create visible micro-shadow in recessed channels and controlled warm soft-satin highlights on local taupe and ivory yarns. Relief must come from over-under interlacing, local compression and return into the ground weave, never inflated beads, smooth contour tubes, independent piping or embroidery. Every visible yarn colour follows the current design region. Keep coarse raised crowns vertical, fine cross yarns horizontal and fine ground/anchoring threads recessed in upright rug coordinates; never rotate crown axes to follow motif paths.

Material identity check: the visible surface must match the construction lock and scale behaviour. Repeated identical raised units without visible support, compression or interlacing fail the material check. Reject any visible anti-substitution.

Topology lock: retain motif count, principal boundaries, containment, adjacency, symmetry and negative space. Keep exterior finish outside the artwork when visible.
Corner lock: both adjoining bound edges and their junction must be visible; their directions and nearby motif must match the selected corner in the upright design. Exclusions: historical-reference motifs or colours, added motifs, merged regions, crossed or broken design lines, mirrored or rotated artwork, labels, logos, text, watermark, unrelated props.
```

## Product overview

```text
Use case: carpet product screening
Output: one bright, crisp commercial-product full-product overview
[shared authority block]

Design orientation: upright, matching the design source
Construction orientation: all yarn-system directions are expressed in upright finished-rug coordinates, not raw reference-image axes
Selected detail corner: [upper_left|upper_right|lower_left|lower_right]
Default detail corner: lower_left
Material ID: [material_id]
Construction: [construction]
Reference strength: [reference_strength]
Mapping mode: [mapping_reference_mode]
Construction lock: [orientation_frame; coarse_raised_yarn_axis; fine_cross_yarn_axis; fine_ground_anchor_axis; surface_structure; yarn_geometry; interlacing; grain_direction; scale_behavior; surface_relief; yarn_exposure_balance; boundary_behavior; yarn_colour_behavior; edge_geometry; finish]
Anti-substitutions: [material-specific anti_substitutions]
Colour authority: [colour_authority]
Colour mapping: [colour_mapping or current design-source colours]
Edge finish: [edge_finish]
Photography style: [photography_style]

Generate this overview only after `material_detail` has passed inspection. Use the current design source as the sole authority for the complete rug outline, all motifs, boundaries, negative space and final colours. Use the accepted `material_detail_anchor` only as a texture reference for yarn character, interlacing, relief, boundary behaviour and light response; never let it redraw or replace the artwork. Place the complete rug flat on a simple pale matte floor or subtle porcelain-tile surface. Match a professional standing-observer downward rug-sample photograph with a restrained near-overhead angle, slightly closer framing and only mild natural near-to-far perspective: the near lower edge is just slightly larger than the far upper edge. Keep the rug square to the frame, long axis vertical, short edges horizontal, at most 0–2 degrees residual rotation, all four corners and the complete bound outline visible, and fill about 92–96% of the image with narrow quiet floor margins. Keep the perspective calm, with no diagonal camera roll, dramatic foreshortening, keystone distortion or wide-angle distortion. Use clean neutral textile-catalog lighting, a small soft contact shadow, clear colour separation, crisp medium-high contrast and controlled warm highlights; preserve tactile relief and weave shadows at product distance without hard plastic gloss.

Presentation tone: bright and clean rather than subdued. Avoid a grey veil, muddy low saturation, underexposure, flat low contrast, dim mood lighting, clipped highlights and crushed shadows.

Material identity check: the overview must read as the same physical construction as the detail anchor at a smaller apparent scale. Reject any visible anti-substitution.

Pattern-ground parity lock: inspect a plain field and a patterned boundary at the same apparent scale. Both share one three-system weave and one two-scale vertical crown hierarchy. Coarse vertical crowns remain dominant at about 55–65% visible exposure without closing the surface. Fine horizontal cross yarns remain continuously readable at about 25–35% through the plain field, motif interiors and every colour boundary. Fine vertical ground or anchoring threads remain recessed. Pattern changes colour and local exposure, while yarn scale, balance and interlacing stay integrated.

Topology lock: preserve current outline, motif count and placement, principal boundaries, containment, adjacency, symmetry and negative space. Keep the design upright and make the selected detail corner visible in the same location. A slight camera or rug rotation is allowed for presentation only; do not redesign, mirror, rotate the artwork, or use perspective that hides topology.
Exclusions: historical-reference motifs or colours, added or removed regions, tangled lines, raw edges, fringe unless supplied, mirrored or rotated artwork, unrequested furniture, labels, logos, text, watermark, CGI gloss.
```

## Targeted retry

Use only after the quality gate identifies one failed category and the user requests a retry:

```text
Edit only [failed category or masked area]. Keep the accepted design topology, colours, material construction, texture scale, camera, lighting, background and edge treatment unchanged. Apply this correction: [single repair action from backend-strategies.md].
```

## Profile-only note

For `profile_only`, add:

```text
The construction is a provisional generic visual profile. Render only observable profile traits and do not imply a specific factory material, fibre, density or process.
```
