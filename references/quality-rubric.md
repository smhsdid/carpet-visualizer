# Lightweight quality rubric

Run this gate once. It identifies caveats; it does not authorize automatic regeneration.

## Preflight

The run is ready when:

- the current design source is legible enough to identify outline and major regions;
- a requested material or valid design-only default is resolved;
- every real or generated reference has one declared role;
- bundled manifest paths exist and selected generation inputs were inspected;
- colour authority is unambiguous;
- a paired example is used only when its exact three-file relationship is established;
- missing real evidence is represented as `profile_only`, not silently invented.

Ask only for a missing design or for material choice when no valid default exists. If artwork is low-resolution, photographed, skewed, or ambiguous, continue when main topology is readable and disclose the limitation.

## Output inspection

Classify each category as `pass`, `caveat`, or `fail`.

| Category | Pass condition | Material failure |
| --- | --- | --- |
| Pattern topology | Current outline, motif count, principal boundaries, adjacency, symmetry and negative space remain recognisable | Large redraw, missing or merged motif, crossed line, invented region |
| Construction | Selected weave or pile family is recognisable at the appropriate scale; raised jacquard crowns visibly bend over, compress against and return between the finer yarn systems with subtle natural variation | Generic plastic, print for weave, pile for flatweave, block or tile artifacts, identical inflated units, or relief disconnected from interlacing |
| Construction orientation | In upright rug coordinates, coarse raised yarns run vertically, fine cross yarns run horizontally, and fine recessed ground or anchoring yarns run vertically after reference rotation or folding is normalised | Raw reference axes are copied; a yarn system is missing; coarse raised yarns run horizontally; cross and ground yarns are conflated |
| Yarn exposure hierarchy | Two related sizes of vertical crown are naturally interleaved; coarse vertical crowns remain dominant at about 55–65% visual exposure while horizontal fine yarns stay continuously readable at about 25–35% in plain, patterned and boundary regions | One uniform vertical crown size; vertical crowns close the surface; horizontal yarns disappear in motif or boundary regions; horizontal share appears only in the plain field |
| Pattern-ground parity | Equal-scale pattern and plain-field areas share one yarn family, coarse-bundle calibre, fine-yarn spacing, three-system interlacing logic, directional rhythm and finish; supported variation in yarn exposure, coverage and relief remains integrated | Smooth printed motif; enlarged rope-like units; long open loops; separately applied embroidery or cord; unrelated pile family; raised elements disconnected from the cross and ground yarn systems |
| Detail localisation | Detail shows the selected upright-design corner, its complete binding junction, both adjacent edges, and recognisable nearby border artwork | Wrong corner, mirror or rotation, missing corner junction, cropped binding, or unlocatable motif |
| Detail texture view | An ultra-close grazing diagonal macro view from about 8–12 degrees above the rug plane fills about 96–98% of the frame; the near binding side face is prominent and strong depth recession, near-to-far scale compression and gentle far-field focus falloff are visible while near and central interlacing remains sharp | High camera position, weak surface recession, small binding side face, uniform yarn scale from near to far, camera too distant, excessive background, missing corner junction, or useful interlacing obscured by blur |
| Cross-scale consistency | Detail and overview share yarn hierarchy, relief, boundary behaviour, edge and light | Different constructions or products |
| Colour authority | Coarse raised, fine cross and fine ground/anchoring yarns all follow the mapped card or local current-design region, with only tone-on-tone variation from light and depth | A fixed pale or white binder grid appears independently of the artwork, or material/historical-reference colours leak into output |
| Reference isolation | Historical examples contribute mapping only; style contributes photography only | Old motifs appear, scene changes material, or quality anchor overrides real evidence |
| Product finish | Edge is continuous and proportionate; corners are finished | Raw edge, discontinuous binding, malformed corner |
| Overview framing | Directly overhead level view; rug is upright, centred, unskewed, fully visible, and fills about 90–95% of the frame with a narrow even margin | Oblique perspective, converging edges, rotation, cropped binding or corners, or excessive background |
| Presentation tone | Bright high-key commercial exposure, luminous whites or light neutrals, clear colours and crisp medium-high contrast retain both highlights and weave shadows | Grey veil, muddy desaturation, underexposure, flat subdued grading, clipped highlights or crushed shadows |
| Scene discipline | Rug dominates a clean commercial catalogue photograph | Unrequested props, text, logos, watermark, dramatic CGI treatment |

Record the result in this shape:

```yaml
evaluation_record:
  topology: pass|caveat|fail
  material: pass|caveat|fail
  construction_orientation: pass|caveat|fail
  yarn_exposure_hierarchy: pass|caveat|fail
  pattern_ground_parity: pass|caveat|fail
  detail_localisation: pass|caveat|fail
  detail_texture_view: pass|caveat|fail
  overview_framing: pass|caveat|fail
  presentation_tone: pass|caveat|fail
  cross_scale_consistency: pass|caveat|fail
  colour_authority: pass|caveat|fail
  edge_finish: pass|caveat|fail
  region_iou: null
  boundary_f_score: null
  colour_delta_e: null
  failure_tags: []
```

Use only these failure tags: `pattern_drift`, `colour_leakage`, `material_substitution`, `construction_orientation_error`, `pattern_material_mismatch`, `detail_camera_error`, `synthetic_relief`, `yarn_balance_error`, `corner_mismatch`, `cross_scale_inconsistency`, `edge_error`, and `authority_leakage`. Numerical fields are optional diagnostic signals for controllable local workflows. Populate them only when the output was compared against derived design controls; they are not manufacturing tolerances.

## Delivery decision

- `pass`: deliver normally.
- `caveat`: deliver both images and name the visible limitation.
- `fail`: deliver only if useful for diagnosis, identify the failed category, and offer one targeted retry. Do not claim the failed image is representative.

Separate-image outputs provide visual consistency, not literal pixel continuity. Material recognisability belongs primarily to the detail; topology and overall product read belong primarily to the overview.

## Targeted retry language

When the user requests a retry, repeat the unchanged render lock and alter only the failed category. Read [backend strategies](backend-strategies.md) for backend-specific repair actions:

- Pattern drift: reinforce current topology and use the current design as edit target again.
- Material drift: reinforce construction and remove conflicting references.
- Construction orientation error: use the stored upright generation-input orientation directly and restate all three axes in upright design-source coordinates: coarse raised vertical, fine cross horizontal, fine ground/anchor vertical.
- Pattern material mismatch: compare equal-scale pattern and field crops; require one shared three-yarn jacquard system while retaining supported variation in exposed bundles and local relief. If the preview backend alternates between printed motifs and unrelated applied or pile-like motifs across two single-variable trials, stop prompt iteration and use a controllable local workflow.
- Detail camera error: move the lens nearly level with the near binding to 8–12 degrees above the rug plane; require a prominent binding side face, strong depth recession, near-to-far scale compression, and gentle far-field focus falloff while the near and central interlacing stays sharp.
- Synthetic relief: retain the accepted topology and rebuild only the textile surface so coarse soft twisted floats visibly bend over horizontal yarns, compress at ties and return into the recessed ground with subtle non-repeating variation.
- Yarn balance error: reduce coarse-crown packing, interleave larger and smaller vertical crowns, and restore continuous horizontal fine-yarn exposure through both plain and patterned regions.
- Cross-scale drift: reuse the accepted detail anchor and reduce overview texture scale.
- Colour drift: restate colour authority and use neutral construction inputs.
- Authority leakage: omit the leaking paired, style, or quality reference.
- Edge failure: keep artwork unchanged and edit only perimeter finish.
- Corner mismatch: regenerate or crop only the detail from the declared corner in the upright overview; retain both adjoining bound edges and recognisable border artwork.
