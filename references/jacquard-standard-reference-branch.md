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
construction photos remain audit evidence only; do not attach them to a render in this branch. Do not attach
a scene-style or quality reference unless the user explicitly adds one.

Keep the two standard images separate. Do not make a composite board, add labels, or place a detail inset
inside the overview reference. Preserve their stored orientation and aspect ratio.

## Branch override

This branch replaces the legacy jacquard prompt path for the selected material. Do not reintroduce fixed
numeric yarn-exposure ratios, filament counts, frayed-end counts, or the durable legacy detail target when
the two standard images are available. Let the anchors decide exact calibre, spacing, relief, fuzz, and finish.
Use only the compact scale-specific fingerprint below to keep their most distinctive structure from being
averaged into generic weave.

## Scale-specific construction fingerprint

- Detail: laid bundles of continuous aligned filaments; every visible filament runs from one tie-down to the
  other while staying beside its neighbours, so the bundle fans wider at mid-span and reconverges at both ties
  into an elongated lozenge crown with uninterrupted lengthwise striations; adjacent crown chains are half-repeat
  staggered; lower horizontal yarns and contact shadows form continuous recessed tracks.
- Overview: a fine vertical crown grain crossed by a subtle horizontal recessed-yarn cadence. Preserve the
  anchor's woven rhythm, but never convert it into fixed periodic dark stripes or borrow its motif layout.

The reference images own the exact strength and spacing of these traits. Text names identity, not measurements.

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

Use these presentation constraints alongside the detail anchor:

```text
professional three-quarter tactile macro, camera 25–35 degrees above the rug plane and diagonally across the
corner; one bound edge leads into depth, the complete corner junction and both binding segments remain visible;
bright clean exposure, shallow side raking light with soft fill, crisp near and central fibres, gentle far-field
softening, minimal neutral background
```

Keep the detail focused on the selected design corner when a corner is requested. Preserve the binding
junction and enough surrounding artwork to locate the crop, while allowing the standard detail anchor to
own the physical surface appearance.

## Overview presentation keywords

Use these concise presentation constraints alongside the overview anchor:

```text
complete upright rug, unrolled and flat, standing-observer restrained near-overhead sample shot; mild near-to-far
perspective, square to frame with long axis vertical and at most 0–2 degrees rotation; complete bound outline and
four corners visible, 92–96% frame coverage with narrow quiet pale floor margins; bright clean exposure and a small
natural contact shadow, no staged props
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
Match their scale-appropriate jacquard construction and edge family.
[detail or overview scale-specific construction fingerprint]
Keep one integral weave.
[detail or overview presentation keywords]
No text, labels or watermarks.
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
- macro crowns retain continuous tie-to-tie filament paths, elongated lozenge envelopes, longitudinal sheen, stagger, and recessed horizontal tracks;
- overview texture retains a subtle horizontal woven cadence without adding motif-independent dark stripes;
- the overview has only the requested quiet floor/tile context and a restrained contact shadow.

If the surface drifts, change the reference attachment or crop before adding more material prose. If the
camera or environment drifts, change only the relevant presentation keyword. Record the failed category
and keep accepted reference and design settings fixed.
