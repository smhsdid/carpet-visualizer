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

Use the current design source plus the two standard texture references. If the backend has a reference
budget, allocate two supporting slots to these assets. Attach the detail anchor first for `material_detail`
and the overview anchor first for `product_overview`; use the other standard image as the second supporting
reference when the backend accepts two images. Keep the reference roles explicit in the prompt.

Generate the pair in this order:

1. `material_detail`: produce the close surface reading from the detail anchor.
2. `product_overview`: produce the complete design from the design source, with the overview anchor owning
   product-scale texture and the detail anchor supporting the same surface family.

When a controllable edit backend can derive a detail from an accepted overview, it may crop and locally
refine the selected corner after the overview passes. Preserve the standard-anchor texture identity during
that refinement.

## Detail presentation keywords

Use these concise presentation constraints alongside the detail anchor:

```text
ultra-close tactile macro, low grazing diagonal camera, lens nearly level with the near rug surface,
approximately 8–12 degrees above the rug plane, surface fills 96–98% of the frame, bright clean high-key
exposure, controlled grazing light, crisp near and central fibre detail, gentle far-field softening, neutral
background only where unavoidable
```

Keep the detail focused on the selected design corner when a corner is requested. Preserve the binding
junction and enough surrounding artwork to locate the crop, while allowing the standard detail anchor to
own the physical surface appearance.

## Overview presentation keywords

Use these concise presentation constraints alongside the overview anchor:

```text
complete upright rug, fully unrolled and flat, direct overhead or barely elevated level product camera,
complete bound outline and four corners visible, long edges aligned with the frame, bright clean exposure,
soft natural contact shadow, simple pale matte floor or porcelain-tile background, very subtle tile or floor
context, restrained ambient environment, no furniture or props, no staged lifestyle scene
```

The floor or tile must remain a quiet support plane: lightly visible, low contrast, and subordinate to the
rug. Use a small believable contact shadow and mild ambient light variation so the overview feels real,
without turning the material reference into a room scene.

## Prompt skeleton

Use this compact structure and fill only the current run's design and camera fields:

```text
Use the current design source as the sole authority for rug outline, motif topology, region placement and final colours.
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
- the detail has the requested close tactile camera and the overview shows the complete outline;
- the overview has only the requested quiet floor/tile context and a restrained contact shadow.

If the surface drifts, change the reference attachment or crop before adding more material prose. If the
camera or environment drifts, change only the relevant presentation keyword. Record the failed category
and keep accepted reference and design settings fixed.
