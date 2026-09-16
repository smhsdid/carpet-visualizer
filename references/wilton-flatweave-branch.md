# Wilton flatweave branch

Use this branch when the selected manifest sets `render_branch: wilton_flatweave`. The user confirms the Wilton flatweave classification. The profile is grounded in the supplied three physical sample sets and deliberately does not infer fibre, density, loom setting, or other manufacturing details.

## Evidence and authority

The full-product photos establish a thin, bound rug with an orderly all-over yarn system. The nine real detail photos establish the visible surface: short, substantial multi-filament yarn bundles form aligned rows; finer threads remain visible between and across the bundle rows; all colour areas use that same low-relief system; and the perimeter has a rounded wrapped binding plus a narrow inner locking line. The AI artwork files are design examples only and have no construction authority.

For the reference-grounded visual route, use these roles:

- `design_source`: literal current geometry and colour authority for both outputs. Keep the full source attached for a detail; do not supply a cropped or extended artwork fragment as a camera-control image.
- one manifest-declared real detail camera-and-relief anchor: focal relationship, viewing direction, foreground-corner placement, edge recession, continuous upper rug plane, near-bundle scale, arched crown cross-section, visible shoulder taper, and inter-unit gap proportion only.
- one manifest-declared accepted quality anchor: approved product-photo polish only: bundle midsection fullness, tapered ends, filament legibility, close-oblique camera, and lighting. It does not establish construction facts.
- one manifest-declared multi-unit micro construction anchor: the observed bundle midsection, tapered ends, multi-filament definition, unit scale, exposed cross yarn, and gap proportion only.
- one manifest-declared grammar tile: audit evidence for product-directional lane staggering and open channels; do not attach it when the micro anchor is attached.
- the remaining real photos: audit and human inspection evidence only. Do not attach several patterned samples to a generation request.

Neither secondary reference has authority over current motifs, region placement, colours, outline, or symmetry. A generated detail that borrows its pattern or palette fails with `authority_leakage` or `colour_leakage`.

## Exact paired-mapping route

Before selecting the normal preview packet, compare the current design SHA-256 with `paired-mappings.json`. When it exactly matches a declared paired design, use the manifest's matching override. Attach the complete current design first, the paired physical product overview second, and the paired physical material detail third. The paired photos may guide product camera, binding proportion, yarn-unit morphology, row cadence, cross-yarn visibility, and finish because they document this exact design. The current design remains the only source-coordinate pattern and colour authority.

Do not attach the generic accepted-quality anchor or generic micro anchor to an exact paired packet: any reference with a different unit scale, bead geometry, or camera relationship is a construction conflict, not an additional quality signal. For unmatched designs, attach the complete current design first, the real camera anchor second, and the micro construction anchor third. The optional quality anchor may control only exposure, white balance, and general product-photo finish.

## Surface contract

Rebuild the visible surface from the design's source-coordinate regions. Do not retain a visible RGB artwork plate under a luminance, normal, emboss, displacement, noise, or generic texture layer. That is `surface_build_mode: overlay` and fails.

In upright product coordinates, principal bundle lanes follow the rug long axis. The lanes are visibly separated by open, shadowed longitudinal channels that expose the finer cross yarns; the channels are not reduced to hairline seams. Each lane is segmented into separate bundles rather than reading as a continuous rib. Every small near-detail area contains both plainly short and plainly longer tapered units, while their ends in neighbouring lanes are offset rather than aligned across a single crosswise grid or a fixed alternation. Finer interlacing threads bridge the offsets and remain visible. Bundle orientation is construction-wide and does not turn to trace a motif. Each colour region contains the same lane structure, length variation, fine threads, low crown height, shallow gaps, and restrained filament highlights. Boundaries change colour at the bundle scale inside this one system; they are not smooth, painted, piped, or independently raised.

The edge has a rounded, continuous colour-matched wrapped binding. Preserve the slim locking line just inside it and carry both treatments cleanly through the corner. The required detail camera rakes across the plane: the selected near corner and binding are foreground, the surface visibly recedes away from them, and closest bundles appear coarser and more raised than distant bundles. This shallow relief comes from side shadows and directional filament highlights, not tall pile. Do not replace the edge with a loose fringe, a raw cut edge, or an oversized rolled cord.

## Detail prompt

```text
Image 1 is the complete literal current design. Preserve every outline, binding, inner lock line, motif line, junction, boundary, negative-space component, colour region, and especially every original perimeter-to-pattern spacing. Image 2 is the real lower-left camera-and-relief anchor: match its focal relationship and framing, near-bundle scale, and visible gaps; it has zero authority over current motifs or colours. Image 3 is a real multi-unit micro construction anchor: match its exact loose multi-filament bundle geometry, exposed fine cross yarn, and gap proportion. Images 2–3 have zero authority over current geometry, region layout, or colours.

Render this exact crop as a low-relief structured woven rug. Reconstruct every visible colour region from product-directional lanes of substantial multi-filament bundles. Segment every lane into distinct units, so the near-detail plane visibly contains both short bundles and longer bundles spanning more vertical distance; neither class is a rare exception. Offset their ends irregularly across neighbouring lanes. Leave clearly readable shadowed longitudinal channels between the lanes; these channels expose finer cross yarns and must remain more open than a hairline seam. Each near-detail unit must be a visibly arched yarn bundle: its central crown is full and wider, while both lateral shoulders taper down into the gap, exactly as Image 2 shows. Keep the same crown profile in the ground, motif, and boundary. Make individual filaments and restrained directional highlights legible at the near plane. The resulting weave is a staggered, ventilated field of yarn units rather than continuous ribs or a repeated bead matrix.

Keep the rounded colour-matched wrapped binding and its slim inner locking line continuous around the complete selected corner. Match Image 2's real focal relationship: the nearest corner and binding are foreground, the left exterior edge recedes upward, near yarn bundles are visibly coarser than distant bundles, and each raised bundle middle has a shallow side shadow. The upper image frame is a crop through the uninterrupted rug plane: it must contain carpet surface, never a horizontal far edge or abrupt cut line. Only a narrow dark textile ground is visible beside genuine selected exterior edges.

Keep the structure target unchanged. The only allowed changes are the declared camera transform and this yarn-built surface. No text or watermark.
```

## Exact paired-mapping detail prompt

```text
Image 1 is the complete current design and the literal source-coordinate target. Images 2 and 3 document a verified physical production of this exact same design: Image 2 is the complete paired product and Image 3 is its paired material detail. Copy Image 1's geometry and colours; Images 2 and 3 control only the physical rendering, camera, binding, and fibre-scale weave.

Render the lower-left corner as the same close oblique product view as the paired physical sample. The left and bottom wrapped edges, the narrow inner lock line, the dense border, the corner junction, and the adjacent diamond field must remain correctly registered to Image 1. Match Image 3 literally at fibre scale: loose multi-filament short yarn bundles with visibly split, slightly fuzzy ends; variable-width and variable-length units; a fine pale cross yarn exposed in the gaps between every few bundles; irregular stagger across neighbouring long-axis lanes; shallow soft shadows rather than a clean bead lattice. The bundle field must be compact and dense, with no smooth capsule grid, continuous vertical ribs, plastic sheen, rope-like binding, embroidery, or texture overlay. Use the paired product's low raking camera, with the near bound corner forward and natural focus falloff across the continuous rug plane. No text or watermark.
```

## Overview prompt

```text
Image 1 is the literal source-coordinate structure target for the full artwork. Copy the rug outline, every motif, boundary, negative-space component, symmetry, and colour region through the declared camera transform. Image 2 is real construction evidence: it controls only the observed low-relief bundle system, fine interlacing visibility, and binding proportion. It has zero authority over current artwork geometry or colours.

Render one complete structured woven rug rebuilt from Image 1's source-coordinate regions. Across every colour region, preserve the same product-directional bundle lanes, open longitudinal channels, cross-yarn interlacing, staggered ends, short-and-long tapered unit variation, low compact relief, and restrained filament highlights. Keep current pattern edges as yarn-colour transitions inside this same surface. Preserve the rounded continuous colour-matched wrapped binding and slim inner locking line around all four corners. Do not display a flat artwork plate with a texture overlay.

Show the complete rug flat on a neutral dark textile ground in a product-record photograph, restrained near-overhead perspective with mild near-to-far scale change, all four bound corners visible, narrow margins, and a small natural contact shadow. No furnishings, text, or watermark.
```

## Acceptance gate

The detail passes only when the aligned proof and anchor register pass, and all of the following are true:

- principal bundle rows remain product-directional across ground and motif rather than following artwork lines;
- open longitudinal channels, adjacent-lane staggering, and both clearly short and clearly longer segmented units remain legible at the detail scale;
- the raking oblique camera gives a clear foreground-to-background scale change and shallow side shadows that make the coarse bundle relief legible;
- bundle size, fine interlacing visibility, low crown height, shallow gaps, and light response are the same across all colour regions;
- the real-reference surface is matched without its motif or palette leaking into the current artwork;
- the wrapped binding, inner lock line, selected corner junction, and both adjacent edges are complete;
- the binding, inner lock line, motifs, and rug outline retain Image 1's original relative positions and spacing, without visible drift, double-registration, or expanded perimeter gap;
- the upper frame remains continuous carpet plane, with no false transverse far edge caused by the detail crop;
- the camera has an evident close oblique recession, rather than blur presented as depth.

Any hard-gate failure stops the overview. A run missing real construction evidence cannot pass. A generic quality anchor is optional and must never override real yarn geometry.

## Reference-grounded visual route

This is the default route for a user-facing visual sample when no exact paired mapping exists. Use the complete current design first, the manifest-declared real detail camera anchor second, and the multi-unit micro construction anchor third. Use the accepted quality anchor only after verifying that its unit geometry and camera do not conflict; it may control only exposure, white balance, and general product-photo finish. The paired mapping sets and grammar tile remain calibration and audit evidence unless the current source exactly matches a declared paired design.

Record this as `topology_mode: approximate` and record all three attachment paths and roles. A visually strong detail may unlock a product overview only after the user accepts it; it must never be relabelled as exact merely because it follows the design approximately.

## Exact-proof route

`scripts/render_wilton_calibrated.py` is restricted to `structure_proof.png` plus topology metadata. Its fixed rounded-bundle synthesis is useful for source-coordinate proof only and is prohibited from producing or being presented as `material_detail` or `product_overview`. A final exact textile render requires an independently controllable material backend with a declared real construction reference.
