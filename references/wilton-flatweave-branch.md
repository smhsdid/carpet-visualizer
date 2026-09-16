# Wilton flatweave branch

Use this branch when the selected manifest sets `render_branch: wilton_flatweave`. The profile is grounded in the supplied three physical sample sets and deliberately does not infer fibre, density, loom setting, or other manufacturing details.

## Evidence and authority

The full-product photos establish a thin, bound rug with an orderly all-over yarn system. The real detail photos establish the visible surface: short, substantial multi-filament yarn bundles form aligned rows; finer threads remain visible between and across the bundle rows; all colour areas use that same low-relief system; and the perimeter has a rounded wrapped binding plus a narrow inner locking line. The artwork files are design examples only and have no construction authority.

For the unified generation route, use these roles:

- `design_source`: literal current geometry and colour authority for both outputs. Keep the full source attached.
- one manifest-declared real detail camera-and-relief anchor: focal relationship, viewing direction, fixed lower-left foreground-corner placement, edge recession, continuous upper rug plane, near-bundle scale, arched crown cross-section, visible shoulder taper, and inter-unit gap proportion only;
- one manifest-declared multi-unit micro construction anchor: bundle midsection, tapered ends, multi-filament definition, unit scale, exposed cross yarn, and gap proportion only;
- one optional `quality_anchor`: exposure, white balance, and general product-photo finish only;
- a grammar tile: audit evidence for product-directional lane staggering and open channels; do not attach it when the micro anchor is attached.

Neither secondary reference has authority over current motifs, region placement, colours, outline, or symmetry. A generated detail that borrows its pattern or palette fails with `authority_leakage` or `colour_leakage` and is recorded in the check result.

Paired mappings are calibration evidence only. Never attach the overview or detail from a pair whose design SHA-256 matches the current source. Use a non-matching generic anchor instead.

## Surface contract

Rebuild the visible surface from the design's source-coordinate regions. Do not retain a visible RGB artwork plate under a luminance, normal, emboss, displacement, noise, or generic texture layer. That is `surface_build_mode: overlay` and fails the material check.

In upright product coordinates, principal bundle lanes follow the rug long axis. The lanes are visibly separated by open, shadowed longitudinal channels that expose finer cross yarns; the channels are not reduced to hairline seams. Each lane is segmented into separate bundles rather than reading as a continuous rib. Every small near-detail area contains both plainly short and plainly longer tapered units, while their ends in neighbouring lanes are offset rather than aligned across a single crosswise grid or a fixed alternation. Finer interlacing threads bridge the offsets and remain visible. Bundle orientation is construction-wide and does not turn to trace a motif.

Each colour region contains the same lane structure, length variation, fine threads, low crown height, shallow gaps, and restrained filament highlights. Boundaries change colour at the bundle scale inside this one system; they are not smooth, painted, piped, or independently raised.

The edge has a rounded, continuous colour-matched wrapped binding. Preserve the slim locking line just inside it and carry both treatments cleanly through the lower-left corner. The detail camera rakes across the plane: the selected corner and binding are foreground, the surface visibly recedes away from them, and closest bundles appear coarser and more raised than distant bundles. This shallow relief comes from side shadows and directional filament highlights, not tall pile.

## Detail prompt

```text
Image 1 is the complete literal current design and sole authority for every outline, binding, inner lock line, motif line, junction, boundary, negative-space component, colour region, and original perimeter-to-pattern spacing. Keep the complete design structure unchanged.

Image 2 is a real lower-left camera-and-relief anchor. Match its focal relationship, framing, near-bundle scale, visible gaps, and continuous rug plane only. It has zero authority over current motifs or colours.

Image 3 is a real multi-unit construction anchor. Match its multi-filament bundle geometry, exposed fine cross yarn, unit scale, and gap proportion only. It has zero authority over current geometry, region layout, or colours.

Render the fixed lower-left corner as a low-relief structured woven rug. Reconstruct every visible colour region from product-directional lanes of substantial multi-filament bundles. Segment every lane into distinct units, with both short and longer tapered units visible in the near-detail plane. Offset their ends irregularly across neighbouring lanes. Leave clearly readable shadowed longitudinal channels between the lanes so finer cross yarns remain visible. Each unit has a full arched middle and shoulders that taper into the gap. Keep the same construction in ground, motif, and boundary regions.

Keep the rounded colour-matched wrapped binding and slim inner locking line continuous around the complete lower-left corner and both adjacent edges. Match the close-oblique raking view: the nearest corner is foreground, one bound edge recedes upward, near bundles are visibly coarser, and the upper frame continues through carpet surface rather than ending at a false horizontal rug edge.

Keep the source pattern and spacing unchanged. No text or watermark.
```

## Overview prompt

```text
Image 1 is the complete literal current design and sole authority for the full artwork. Copy the rug outline, every motif, boundary, negative-space component, symmetry, colour region, binding, and inner locking line without redesign.

Use the declared real construction references only for the low-relief bundle system, fine interlacing visibility, staggered ends, short-and-long tapered unit variation, binding proportion, and restrained filament highlights. Do not import their motifs or palette.

Render one complete structured woven rug rebuilt from Image 1's source-coordinate regions. Across every colour region, preserve the same product-directional bundle lanes, open longitudinal channels, cross-yarn interlacing, staggered ends, low compact relief, and restrained filament highlights. Do not display a flat artwork plate with a texture overlay.

Show the complete rug flat on a neutral dark textile ground in a product-record photograph, restrained near-overhead perspective with mild near-to-far scale change, all four bound corners visible, narrow margins, and a small natural contact shadow. No furnishings, text, or watermark.
```

## Lightweight detail check

Run one compact check after the detail is generated and before the overview call. Confirm that the file opens, the lower-left corner and both bound edges are visible, the upper frame continues through rug surface, the pattern remains recognisable and registered, the same yarn system appears in ground and motif, and there is no obvious flat texture overlay or reference-pattern leakage.

Record each item as `pass`, `caveat`, or `fail`. A visual caveat does not require user confirmation and does not stop the overview. Only a missing, unreadable, or technically invalid detail stops the sequence.

## Unified route

Use the complete current design first, the declared generic detail camera-and-construction anchor second, and the multi-unit micro construction anchor third. Attach the optional quality anchor only when it fits the backend budget; it controls finish only. Generate the detail, save the actual prompt and parameters, run the lightweight check, and automatically generate the overview. Record all actual attachments and their hashes.

The deterministic helper is diagnostic only. It must never be presented as the material detail or product overview.
