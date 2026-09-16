# Wilton flatweave branch

Use this branch when the selected manifest sets `render_branch: wilton_flatweave`. The user confirms the Wilton flatweave classification. The profile is grounded in the supplied three physical sample sets and deliberately does not infer fibre, density, loom setting, or other manufacturing details.

## Evidence and authority

The full-product photos establish a thin, bound rug with an orderly all-over yarn system. The nine real detail photos establish the visible surface: short, substantial multi-filament yarn bundles form aligned rows; finer threads remain visible between and across the bundle rows; all colour areas use that same low-relief system; and the perimeter has a rounded wrapped binding plus a narrow inner locking line. The AI artwork files are design examples only and have no construction authority.

For an exact run, use these roles:

- `design_detail_crop` or `design_source`: literal structure and colour authority.
- one manifest-declared real construction image: the observed bundle scale, row cadence, fine-thread visibility, relief, edge, and camera authority only.
- the remaining real photos: audit and human inspection evidence only. Do not attach several patterned samples to a generation request.

The real construction image has zero authority over current motifs, region placement, colours, outline, or symmetry. A generated detail that borrows its pattern or palette fails with `authority_leakage` or `colour_leakage`.

## Surface contract

Rebuild the visible surface from the design's source-coordinate regions. Do not retain a visible RGB artwork plate under a luminance, normal, emboss, displacement, noise, or generic texture layer. That is `surface_build_mode: overlay` and fails.

In upright product coordinates, principal short bundle rows follow the rug long axis. Finer interlacing threads cross and separate them. Bundle orientation is construction-wide and does not turn to trace a motif. Each colour region contains the same rows, fine threads, low crown height, shallow gaps, and restrained filament highlights. Boundaries change colour at the bundle scale inside this one system; they are not smooth, painted, piped, or independently raised.

The edge has a rounded, continuous colour-matched wrapped binding. Preserve the slim locking line just inside it and carry both treatments cleanly through the corner. Do not replace it with a loose fringe, a raw cut edge, or an oversized rolled cord.

## Detail prompt

```text
Image 1 is the literal source-coordinate structure target for the [lower-left] artwork crop. Copy every motif line, junction, boundary, negative-space component, colour region, and corner identity through the declared camera transform. Image 2 is a real construction reference. Image 2 controls only the observed yarn-built surface, rounded bound edge, and close-oblique product camera; it has zero authority over current geometry, region layout, or colours.

Render this exact crop as a low-relief structured woven rug. Reconstruct every visible colour region from regular, substantial short multi-filament yarn bundles aligned in rows along the rug long axis. Keep the same compact, slightly flattened bundle crowns in the ground, motif, and boundary. Between and across the rows, show finer interlacing threads and shallow shadowed gaps. Make individual filaments and restrained directional highlights legible at the near plane. Preserve a consistent bundle scale: not a smooth colour field, a tiny bead grid, a basket weave, tall pile, loose loop pile, ropes, or a separate raised motif layer.

Keep the rounded colour-matched wrapped binding and its slim inner locking line continuous around the complete selected corner. Use Image 2's close oblique viewing relationship: the nearest corner and binding are prominent, one exterior edge recedes diagonally, near yarn bundles are visibly larger than distant bundles, the rug plane is unrectified, and only a narrow pale-floor strip is visible.

Keep the structure target unchanged. The only allowed changes are the declared camera transform and this yarn-built surface. No text or watermark.
```

## Overview prompt

```text
Image 1 is the literal source-coordinate structure target for the full artwork. Copy the rug outline, every motif, boundary, negative-space component, symmetry, and colour region through the declared camera transform. Image 2 is a real construction reference. It controls only the observed low-relief bundle system, fine interlacing visibility, binding proportion, and clean product presentation; it has zero authority over current artwork geometry or colours.

Render one complete structured woven rug rebuilt from Image 1's source-coordinate regions. Across every colour region, preserve the same aligned rows of short multi-filament yarn bundles, the fine interlacing threads in their gaps, low compact relief, and restrained filament highlights. Keep current pattern edges as yarn-colour transitions inside this same surface. Preserve the rounded continuous colour-matched wrapped binding and slim inner locking line around all four corners. Do not display a flat artwork plate with a texture overlay.

Show the complete rug flat on a pale floor in a bright commercial product photograph, restrained near-overhead perspective, all four bound corners visible, narrow floor margins, and a small natural contact shadow. No text or watermark.
```

## Acceptance gate

The detail passes only when the aligned proof and anchor register pass, and all of the following are true:

- principal bundle rows remain product-directional across ground and motif rather than following artwork lines;
- bundle size, fine interlacing visibility, low crown height, shallow gaps, and light response are the same across all colour regions;
- the real-reference surface is matched without its motif or palette leaking into the current artwork;
- the wrapped binding, inner lock line, selected corner junction, and both adjacent edges are complete;
- the camera has an evident close oblique recession, rather than blur presented as depth.

Any hard-gate failure stops the overview. A `reference_limited` run cannot pass the construction-reference or close-oblique-camera checks.
