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
| Construction | Selected weave or pile family is recognisable at the appropriate scale | Generic plastic, print for weave, pile for flatweave, block or tile artifacts |
| Cross-scale consistency | Detail and overview share yarn hierarchy, relief, boundary behaviour, edge and light | Different constructions or products |
| Colour authority | Colours follow mapped card or current design | Material or historical-reference colours leak into output |
| Reference isolation | Historical examples contribute mapping only; style contributes photography only | Old motifs appear, scene changes material, or quality anchor overrides real evidence |
| Product finish | Edge is continuous and proportionate; corners are finished | Raw edge, discontinuous binding, malformed corner |
| Scene discipline | Rug dominates a restrained product photograph | Unrequested props, text, logos, watermark, dramatic CGI treatment |

## Delivery decision

- `pass`: deliver normally.
- `caveat`: deliver both images and name the visible limitation.
- `fail`: deliver only if useful for diagnosis, identify the failed category, and offer one targeted retry. Do not claim the failed image is representative.

Built-in preview outputs provide visual consistency, not literal pixel continuity. Material recognisability belongs primarily to the detail; topology and overall product read belong primarily to the overview.

## Targeted retry language

When the user requests a retry, repeat the unchanged render lock and alter only the failed category:

- Pattern drift: reinforce current topology and use the current design as edit target again.
- Material drift: reinforce construction and remove conflicting references.
- Cross-scale drift: reuse the accepted detail anchor and reduce overview texture scale.
- Colour drift: restate colour authority and use neutral construction inputs.
- Authority leakage: omit the leaking paired, style, or quality reference.
- Edge failure: keep artwork unchanged and edit only perimeter finish.
