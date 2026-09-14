# Prompt templates

Use concise English prompts for the image model. Replace bracketed fields with the render lock and omit absent optional blocks. The current design source is always the edit target.

## Shared authority block

```text
Image roles are strict. The current design source is the only authority for current outline, motif geometry, placement and default colours. A mapped colour card overrides only mapped colour regions. Construction references control only their declared physical traits and have no colour or motif authority. A paired historical example teaches only how artwork translates into this construction; never copy its motif, layout or palette. A scene-style reference controls only camera, lighting, background and crop. A quality anchor controls polish only.
```

## Corner material detail

```text
Use case: carpet material screening
Output: one bright, crisp commercial-product material close-up
[shared authority block]

Design orientation: upright, matching the product overview; no mirror or rotation
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

Create an ultra-close macro commercial-product photograph of the selected physical rug corner. Place the lens nearly level with and just above the near binding, roughly 8–15 degrees above the rug plane, and aim diagonally across the surface. Make the near binding side face prominent, with strong surface recession, distinct near-to-far yarn-scale compression and gentle distant focus falloff. Move close enough that rug surface fills about 94–98% of the frame. Keep the complete near corner junction, very short segments of both adjoining bindings, and only enough nearby border motif to locate the crop. Use bright high-key grazing light to reveal fibre-scale self-shadowing and keep the near and central interlacing sharp.

The camera treatment is independent from material identity. A one-time scene reference may guide distance, angle, crop, focus falloff and lighting only. In the perspective-rectified rug, coarse raised crowns run vertically and dominate without closing the weave. Use two related vertical crown scales: larger dominant crowns and smaller secondary crowns about 1.3–1.6 times narrower, naturally interleaved. Keep coarse crowns at about 55–65% visual exposure. Finer horizontal cross yarns remain continuously readable at about 25–35% through plain fields, motif interiors and colour boundaries; fine vertical ground or anchoring threads remain visible in recessed channels. Build relief through over-under interlacing, local compression and return into the ground weave. Every visible yarn colour follows the current design region.

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

Place the complete rug flat in a clean bright commercial catalogue setting on a warm-white or light neutral surface. Use a directly overhead, level camera with the sensor plane parallel to the rug plane: no oblique view, no converging edges, and no visible near-side perspective. Keep the upright rug centred with its long edges parallel to the frame. Match the canvas to the rug aspect ratio where possible and fill about 90–95% of the image, leaving only a narrow, even margin while keeping the entire bound outline and all four corners visible. Use high-key directional studio daylight, clean exposure, clear colour separation, crisp medium-high contrast and a narrow defined contact shadow. At this distance, reduce the apparent size of individual bundles while preserving the locked coarse-raised, fine-cross and fine-ground yarn hierarchy, relief distribution, boundary behaviour, edge geometry and light direction; the surface must still read as tactile woven jacquard rather than becoming smooth. Keep fibre highlights clear and luminous according to the locked finish without hard plastic gloss.

Presentation tone: bright and clean rather than subdued. Avoid a grey veil, muddy low saturation, underexposure, flat low contrast, dim mood lighting, clipped highlights and crushed shadows.

Material identity check: the overview must read as the same physical construction as the detail anchor at a smaller apparent scale. Reject any visible anti-substitution.

Pattern-ground parity lock: inspect a plain field and a patterned boundary at the same apparent scale. Both share one three-system weave and one two-scale vertical crown hierarchy. Coarse vertical crowns remain dominant at about 55–65% visible exposure without closing the surface. Fine horizontal cross yarns remain continuously readable at about 25–35% through the plain field, motif interiors and every colour boundary. Fine vertical ground or anchoring threads remain recessed. Pattern changes colour and local exposure, while yarn scale, balance and interlacing stay integrated.

Topology lock: preserve current outline, motif count and placement, principal boundaries, containment, adjacency, symmetry and negative space. Keep the design upright and make the selected detail corner visible in the same location. Preserve a rectified overhead presentation without redesigning, mirroring, rotating or perspective-skewing the rug.
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
