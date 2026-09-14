# Prompt templates

Use concise English prompts for the image model. Replace bracketed fields with the render lock and omit absent optional blocks. The current design source is always the edit target.

## Shared authority block

```text
Image roles are strict. The current design source is the only authority for current outline, motif geometry, placement and default colours. A mapped colour card overrides only mapped colour regions. Construction references control only their declared physical traits and have no colour or motif authority. A paired historical example teaches only how artwork translates into this construction; never copy its motif, layout or palette. A scene-style reference controls only camera, lighting, background and crop. A quality anchor controls polish only.
```

## Material detail

```text
Use case: carpet material screening
Output: one photorealistic material close-up
[shared authority block]

Material ID: [material_id]
Construction: [construction]
Reference strength: [reference_strength]
Mapping mode: [mapping_reference_mode]
Construction lock: [copy every construction_lock field]
Colour authority: [colour_authority]
Colour mapping: [colour_mapping or current design-source colours]

Create a close perpendicular or lightly oblique view around a representative boundary in the current artwork. Show the same physical construction on both colour regions and a believable textile transition. Make yarn or pile structure, restrained relief, fibre irregularity and light direction readable. Preserve the current boundary at product scale while allowing only fibre-scale softness.

Topology lock: retain motif count, principal boundaries, containment, adjacency, symmetry and negative space. Keep exterior finish outside the artwork when visible.
Exclusions: historical-reference motifs or colours, added motifs, merged regions, crossed or broken design lines, labels, logos, text, watermark, unrelated props.
```

## Product overview

```text
Use case: carpet product screening
Output: one photorealistic full-product overview
[shared authority block]

Material ID: [material_id]
Construction: [construction]
Reference strength: [reference_strength]
Mapping mode: [mapping_reference_mode]
Construction lock: [copy every construction_lock field]
Colour authority: [colour_authority]
Colour mapping: [colour_mapping or current design-source colours]
Edge finish: [edge_finish]
Photography style: [photography_style]

Place the complete rug flat in the selected restrained product-photography setting. By default use a quiet warm-neutral matte floor, the rug occupying about three quarters of the frame, a lightly elevated 20–30 degree downward view, natural restrained perspective, nearly parallel long edges, one visible near edge, soft directional daylight and a narrow contact shadow. Compress the accepted detail anchor into a coherent textile at overview distance while retaining its construction hierarchy, relief distribution, boundary behaviour, edge geometry and light direction.

Topology lock: preserve current outline, motif count and placement, principal boundaries, containment, adjacency, symmetry and negative space. Perspective may place the rug naturally but may not redesign it.
Exclusions: historical-reference motifs or colours, added or removed regions, tangled lines, raw edges, fringe unless supplied, unrequested furniture, labels, logos, text, watermark, CGI gloss.
```

## Profile-only note

For `profile_only`, add:

```text
The construction is a provisional generic visual profile. Render only observable profile traits and do not imply a specific factory material, fibre, density or process.
```
