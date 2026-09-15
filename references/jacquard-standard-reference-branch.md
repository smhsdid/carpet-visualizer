# Jacquard standard-reference branch

Use this branch when the selected material manifest sets `render_branch: standard_reference_jacquard`.
It is a reference-led rendering path. The two approved standard images are the primary authority for
visible jacquard texture; prose supplies only camera, exposure, framing, and the small amount of scene
context needed for the deliverable.

## Reference packet

Use exactly these two standard assets as construction evidence:

- `standard_texture_references.detail.file`: the fine-surface and interlacing anchor.
- `standard_texture_references.overview.file`: the product-scale, repetition, density, direction, and edge anchor.

The current `design_source` remains the only authority for the current rug outline, motif topology,
region placement, and final colours. The standard images are not colour or motif references. The original
construction photos and the older neutral derivatives remain audit evidence only; do not attach them to a
render in this branch. Do not attach a scene-style or quality reference unless the user explicitly adds one.

Keep the two standard images separate. Do not make a composite board, add labels, or place a detail inset
inside the overview reference. Preserve their stored orientation and aspect ratio.

## Branch override

This branch replaces the legacy jacquard prompt path for the selected material. Do not reintroduce fixed
numeric yarn-exposure ratios, a long enumerated fibre recipe, or the durable legacy detail target when
the two standard images are available. Let the anchors decide the visible yarn calibre, repeat rhythm,
interlacing, relief, fuzz, and finish. Text is a camera and presentation lock, not a second material design.

## Generation packet

Use the current design source plus the two standard texture references. Also prepare a deterministic
`design_detail_crop` from the current source for the selected corner; it is a pattern-only derivative, not a
third construction reference. If the backend has a reference budget, allocate the two supporting slots to the
standard assets and use the crop in the pattern-control slot when available. Keep all reference roles explicit
in the prompt: the current source/crop own motifs and colours, standard images own construction, and the
accepted overview owns detail geometry and cross-scale consistency.

Generate the pair in this order when exact motif matching is important:

1. `product_overview`: produce the complete design from the design source first. Inspect its topology and
   camera, then retain it as `overview_anchor` only when the current outline, motif count, corners, adjacency,
   symmetry, negative space and colours pass.
2. `material_detail`: derive the close surface reading from the accepted `overview_anchor` plus a deterministic
   `design_detail_crop` made from the current source. The crop is the local motif authority; the overview is the
   geometry and cross-scale anchor; standard images control construction only. Never ask the model to infer the
   selected corner from the full artwork alone.

When a controllable edit backend can derive a detail from an accepted overview, it may crop and locally
refine the selected corner after the overview passes. Preserve the standard-anchor texture identity during
that refinement.

## Detail presentation keywords

Use these concise presentation constraints alongside the detail anchor:

```text
professional three-quarter tactile macro, camera approximately 25–35 degrees above the rug plane,
azimuth 20–35 degrees across the two adjoining edges, the corner and one bound edge form a diagonal leading
line into depth, complete near corner junction and both binding segments visible, bright clean high-key exposure,
shallow side raking light plus soft fill, crisp near and central fibre detail, gentle far-field softening, neutral
background only where unavoidable; avoid flat straight-down and extreme near-zero grazing views
```

Keep the detail focused on the selected design corner when a corner is requested. Preserve the binding
junction and enough surrounding artwork to locate the crop, while allowing the standard detail anchor to
own the physical surface appearance.

## Overview presentation keywords

Use these concise presentation constraints alongside the overview anchor:

```text
complete upright rug, fully unrolled and flat on the floor, professional standing-observer downward sample-shot,
restrained near-overhead angle with slightly closer framing and only mild natural near-to-far perspective; the near
lower edge is just slightly larger than the far upper edge, rug square to the frame with at most 0–2 degrees residual
rotation; keep the long axis vertical and the short edges horizontal, complete bound outline and four corners visible,
fill about 92–96% of the frame with narrow quiet floor margins, calm perspective without dramatic foreshortening or
keystone distortion, bright clean exposure, soft natural contact shadow, simple pale matte floor or porcelain-tile
background, restrained ambient environment, no furniture or props, no staged lifestyle scene
```

The floor or tile must remain a quiet support plane: lightly visible, low contrast, and subordinate to the
rug. Use a small believable contact shadow and mild ambient light variation so the overview feels real,
without turning the material reference into a room scene.

## Prompt skeleton

Use this compact structure and fill only the current run's design and camera fields:

```text
Use the current design source as the sole authority for rug outline, motif topology, region placement and final colours.
Use the deterministic design_detail_crop as the sole local pattern authority for the selected detail corner.
Use the attached standard detail and standard overview images as the primary and only construction references.
Match their visible jacquard surface, texture scale, density, direction, relief, fibre character and edge family.
Do not invent a second material system and do not borrow motifs or colours from the references.
[detail or overview presentation keywords]
Preserve the design source exactly and keep the output free of text, labels and watermarks.
```

For the overview, append the overview presentation keywords and keep the subtle floor/tile support plane.
For the detail, append the detail presentation keywords and keep the crop local and tactile.

## Acceptance gate

Pass only when:

- the output's visible surface is recognisably the same construction family as the selected standard anchors;
- detail and overview share one texture identity and compatible scale behaviour;
- the design source still owns all motifs, boundaries, colours, and negative space;
- the detail uses an attractive three-quarter macro angle with a diagonal leading edge and complete corner;
- the overview reads like a standing-observer downward sample photograph with a restrained near-overhead angle, mild
  top-to-bottom perspective, 92–96% frame coverage, only 0–2 degrees residual rotation and complete outline;
- raised and recessed weave layers have visible micro-shadow and controlled warm yarn highlights;
- the overview has only the requested quiet floor/tile context and a restrained contact shadow.

If the surface drifts, change the reference attachment or crop before adding more material prose. If the
camera or environment drifts, change only the relevant presentation keyword. Record the failed category
and keep accepted reference and design settings fixed.
