# Behavioural test cases

Use generated images and the quality rubric as evidence. A wording match is not a test result.

## Test artwork

Prefer one source design with a large region, narrow line, curved two-colour boundary, asymmetric element, and artwork near the perimeter. Reuse it across constructions.

## Case 1: design-only default

Input: only the test artwork.

Expected:

- `jacquard-01` is selected without asking a construction question;
- its manifest and neutral generation inputs are inspected;
- `reference_strength` is `library_grounded`;
- one detail and one overview are generated without an approval pause;
- the unspecified detail corner defaults to `lower_left`;
- the detail uses a close low-oblique macro view to reveal texture layers, while the overview is directly overhead and level;
- the complete rug fills about 90–95% of the overview frame without cropping its binding or corners;
- both outputs use clean high-key exposure, clear colours and crisp medium-high contrast without a grey veil or muddy desaturation;
- bundled reference colours and patterns do not leak.

## Case 2: flatwoven without material photos

Input: test artwork and explicit `flatwoven`; no material reference or colour card.

Expected:

- `reference_strength` is `profile_only` and confidence is `provisional`;
- detail reads as low-profile warp-and-weft rather than pile or print;
- overview retains current topology.

## Case 3: task-reference jacquard

Input: same artwork, `jacquard`, and task-specific photos with explicit roles.

Expected:

- `reference_strength` is `task_reference_grounded`;
- construction lock contains only role-supported observations;
- reference-product colours and motifs do not leak;
- both outputs show one woven construction at different scales.

## Case 4: partial reference pack

Input: artwork, `jacquard`, and only a macro photo.

Expected:

- macro controls yarn geometry and local interlacing;
- missing density, thickness, and binding evidence is disclosed;
- no manufacturing values are invented.

## Case 5: exact paired mapping

Input: current artwork plus one exact historical trio for the selected material.

Expected:

- mapping mode is `paired_mapping_grounded`;
- historical trio influences boundary softening and cross-scale translation;
- current design remains the only current-pattern authority;
- historical motifs and colours do not appear.

## Case 6: unpaired historical product

Input: current artwork and a real product overview without its exact historical design.

Expected: the photo is classified as construction-scale or scene-style evidence, never as a paired mapping example.

## Case 7: topology and colour stress

Input: artwork whose palette and motif differ strongly from all real references.

Expected:

- no principal motif is added, removed, merged, or split;
- fibre-scale softness does not become broad redraw;
- current colours remain unless an explicit mapped colour card overrides them.

## Case 8: Codex invocation

Input: “Use this carpet artwork to make a bright, clear product overview and texture detail.”

Expected: the skill is selected implicitly, uses the design-only default, and returns two outputs without an approval pause.

## Case 9: generic-agent fallback

Input: the same artwork in an agent environment with repository access but no image-generation backend.

Expected:

- the agent reads the generic adapter and capability profile;
- output is labelled `external_execution_required`;
- the packet includes two final prompts, the render lock, ordered attachments, and the quality gate;
- it does not imply that images were generated.

## Case 10: preview reference budget

Input: design artwork plus macro, product-scale, overall-edge, scene, and quality references.

Expected:

- strategy is `preview_only` when independent controls are unavailable;
- the design source remains attached outside the supporting-reference budget;
- at most three supporting references are selected by declared role;
- non-square inputs preserve their useful evidence through padding or a role-specific crop;
- omitted references and their roles are disclosed.

## Case 11: controllable local isolation

Input: the stress artwork and neutral material references in a backend with region, edge, image-reference, mask, and seed controls.

Expected:

- region and edge maps receive only current-design structure;
- material references enter only the material branch;
- independent control values and seed are recorded;
- a perimeter defect is repaired with a perimeter mask rather than a full redraw;
- one experimental comparison changes only one control value.

## Case 12: material scale and substitution

Input: the stress artwork with `jacquard-01`.

Expected:

- tapered, slightly irregular soft multi-filament crowns repeat end-to-end in vertical chains, with naturally interleaved larger and smaller crown scales;
- in upright rug coordinates, coarse raised yarns run vertically, finer cross yarns run horizontally, and fine recessed ground or anchoring yarns also run vertically beneath the crowns;
- coarse vertical crowns remain dominant at about 55–65% visible exposure while horizontal fine yarns remain continuously readable at about 25–35% through plain, patterned and boundary regions;
- all three yarn systems follow the local design-region colour, without a fixed pale or white binder grid;
- clearly pronounced but compact local relief is visibly produced by over-under interlacing, compression at ties and return into the recessed ground while the overall rug body remains thin;
- those bundles reduce in apparent size but remain tactile and woven in the overview;
- equal-scale crops from a plain field and a patterned boundary share one yarn family, coarse-bundle calibre, fine-yarn spacing, three-system interlacing logic, directional rhythm and finish;
- reference-supported variation in yarn exposure, coverage and relief distribution passes when every raised element remains integrated with the same cross and ground yarn systems;
- a smooth printed motif, enlarged rope-like units, long open loops, or separately applied embroidered, corded or unrelated pile-like motif fails `pattern_ground_parity`;
- the surface remains integral relief-rich jacquard rather than print, uniform tufted loop pile, fur, loose chunky knit, crochet, freestanding rope, basket weave, or blocks;
- a failure is recorded under one standard failure tag and routes to one targeted repair.

The bundled product-scale and overall generation inputs are stored with upright pixels and no EXIF orientation dependency. Use their displayed axes directly without another rotation.

If two preview-only single-variable trials alternate between printed and unrelated applied or pile-like pattern failures, expected behaviour is to stop prompt-only retries, record `pattern_material_mismatch`, and route to `controllable_local`.

## Case 13: corner-localised detail

Input: asymmetric upright artwork and `detail_corner: lower_left`.

Expected:

- the overview keeps the design upright without mirroring or rotation;
- the detail shows the physical lower-left corner, including the complete corner junction and both adjoining bound edges;
- adjacent border artwork and colour boundaries make the crop locatable in the overview;
- construction remains readable despite the wider contextual framing;
- a wrong, mirrored, rotated, or cropped-out corner is tagged `corner_mismatch`.

## Case 14: default camera split

Input: upright artwork with no corner or camera instruction.

Expected:

- the detail anchors to `lower_left` and uses an ultra-close grazing diagonal macro view roughly 8–12 degrees above the rug plane;
- the rug surface fills about 96–98% of the detail while the complete near corner junction and short segments of both bindings remain visible;
- the prominent near binding side face, strong depth recession, near-to-far scale compression and gentle focus falloff prove the camera is nearly level with the rug surface;
- grazing light makes yarn organisation, interlacing, pronounced local relief and boundary construction readable across the near and central focus area;
- the overview uses a directly overhead level view with no converging edges or visible near side;
- the rug remains upright, centred, fully visible and fills about 90–95% of the frame with a narrow even margin.

## Case 15: bright commercial presentation

Input: design-only artwork with no requested scene or mood.

Expected:

- both outputs use bright high-key commercial-product lighting and clean exposure;
- whites or light neutrals remain luminous, colours remain clear, and tonal separation is medium-high contrast;
- weave recesses remain visible without turning the whole image grey or underexposed;
- fibre highlights retain detail without clipping or becoming hard plastic gloss.

## Case 19: self-contained jacquard detail target

Input: design-only artwork with bundled `jacquard-01`, no task-specific scene image.

Expected:

- the agent reads `references/jacquard-detail-target.md` before generating the detail;
- the default reference packet uses the current artwork and neutral construction inputs, with no implicit image carried from an earlier conversation turn;
- the detail reproduces the low diagonal 8–12 degree camera, 96–98% surface coverage, prominent near binding side face, strong recession, and gentle far-field focus falloff;
- the visible surface retains two-scale vertical crowns, continuous horizontal fine-yarn exposure, recessed vertical ground threads, and compact interlaced relief;
- diagonal or stepped artwork lines may show stronger local crown exposure but remain integrated into the same weave, with vertical crown axes and crossing horizontal fine yarns rather than a separate smooth contour tube;
- the result remains bright and crisp without requiring a scene-style reference.

## Case 16: stored upright orientation reference

Input: upright artwork and the bundled `jacquard-01` product-scale and overall generation inputs, whose pixels are already stored in upright finished-rug orientation.

Expected:

- the stored upright generation-input axes are used directly without an additional rotation;
- the generated upright rug shows compact coarse raised yarns running vertically, fine cross yarns running horizontally, and fine recessed ground/anchoring yarns running vertically;
- cross and ground yarn colours follow each local design region instead of becoming a global pale grid;
- the same product-relative construction direction appears in the lower-left detail and directly overhead overview;
- an output with horizontal raised floats is tagged `construction_orientation_error`.

## Case 17: reject high-angle synthetic detail

Input: a generated lower-left detail whose corner is locatable but whose rug plane reads nearly overhead and whose raised units are repeated identical capsules.

Expected:

- the image fails `detail_texture_view` with `detail_camera_error` because the near binding side face, depth recession and near-to-far scale compression are absent;
- the image fails construction with `synthetic_relief` because raised units do not visibly bend over, compress against and return between the finer yarn systems;
- it is not accepted as `material_detail_anchor` and cannot control the overview.

## Case 18: preserve supporting horizontal yarns

Input: a `jacquard-01` detail containing both a plain field and a patterned boundary.

Expected:

- larger and smaller vertical crowns are visibly interleaved within one yarn family;
- vertical crowns dominate without closing the woven surface;
- fine horizontal yarns remain continuously readable through the plain field, motif interior and colour boundary;
- a result whose patterned area becomes nearly all coarse vertical crowns fails `yarn_exposure_hierarchy` with `yarn_balance_error`.

## Case 20: standard-reference jacquard branch

Input: test artwork with `jacquard-01` whose manifest declares `render_branch: standard_reference_jacquard`.

Expected:

- the manifest resolves exactly two standard texture references: one detail anchor and one overview anchor;
- the selected standard images are the primary visible-texture authority, while the current design remains the only motif, region and final-colour authority;
- the original construction photos, older neutral derivatives, scene references and quality anchors are not attached unless the user explicitly adds them;
- the branch does not apply the legacy fixed yarn-ratio recipe or durable legacy detail target;
- the detail uses the branch's low-grazing tactile macro keywords and the overview uses its complete-outline keywords;
- the overview has only a quiet pale floor or porcelain-tile support plane with a restrained natural contact shadow;
- detail and overview remain recognisably one surface family at their respective scales.
