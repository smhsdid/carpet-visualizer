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

Input: “Use this carpet artwork to make a realistic product overview and material detail.”

Expected: the skill is selected implicitly, uses the design-only default, and returns two outputs without an approval pause.

## Case 9: generic-agent fallback

Input: the same artwork in an agent environment with repository access but no image-generation backend.

Expected:

- the agent reads the generic adapter and capability profile;
- output is labelled `external_execution_required`;
- the packet includes two final prompts, the render lock, ordered attachments, and the quality gate;
- it does not imply that images were generated.
