# Exact topology lock

Pattern fidelity is a data-integrity requirement, not a style preference. The
current `design_source` is the literal source of the rug's structure. Words such
as “similar”, “recognisable”, “inspired by”, or “preserve generally” are not
valid evidence for an exact run.

## Modes

`topology_mode: exact` is the default for an uploaded artwork. In this mode the
output must retain, in the source coordinate frame, the silhouette, every
principal boundary, motif instance and repeat order, junction connectivity,
containment, negative-space components, symmetry, and mapped colour region.
Camera perspective may transform those coordinates only through the declared
render transform. It may not redraw, merge, split, invent, omit, mirror, or
reorder visible artwork.

Use `topology_mode: approximate` only when the user explicitly accepts a
conceptual approximation. Approximate output must be labelled as such and can
never receive `pattern_gate: pass` or be used as a texture anchor for an exact
run.

## Capability gate

Reference-image input is not structure control. A prompt is not a mask, a
region map, an edge map, or a proof.

| Backend evidence | Exact-mode decision |
| --- | --- |
| Deterministic compositor or controllable structure branch with region/edge controls, plus an aligned proof | Allowed |
| Image editing with a real structure-preserving mask, plus an aligned proof | Allowed only after the proof passes |
| Preview-only semantic generation or reference-only image generation | Unsupported; fail closed |
| Any backend where the agent cannot produce aligned proof evidence | Unsupported; fail closed |

In exact mode, an unsupported backend sets `pattern_control: unavailable`,
`pattern_gate: fail`, `anchor_status: rejected`, and `failure_tags:
[pattern_drift]`. It must not generate `product_overview`. Return
`external_execution_required` with the packet needed by a controllable renderer.

## Deterministic preflight

For a local raster, run:

```text
python scripts/prepare_design_controls.py <design_source> <control_dir> --corner <detail_corner>
```

Keep the original source, its SHA-256, and the generated `design_lock.json`.
The control directory contains the exact corner crop, a pattern-only region
mask, and full/detail edge maps. These files are structural controls and audit
evidence; construction references never replace them.

Before prompting, make an anchor register from the source and its controls. At
minimum enumerate the outer outline, each selected-corner junction, each
visible repeat in the detail crop, the inner boundary, enclosed field, and
every colour transition. Record source-coordinate positions and adjacency.

## Proof-before-render

In an exact controllable workflow:

1. Produce `structure_proof` in the source coordinate frame using only the
   current design controls. Do not add yarn, perspective, lighting, or a
   construction reference yet.
2. Run:

   ```text
   python scripts/validate_topology.py <design_source> <structure_proof> --aligned
   ```

   The command must exit `0`. It compares coarse region labels and boundaries
   with strict thresholds; a perspective product image is not a valid proof.
3. Only after the proof passes may the material branch add the selected surface
   construction or the camera branch add perspective. Preserve the proof as an
   immutable structure input.
4. Inspect the final detail against the anchor register after inverse-mapping
   it to source coordinates. Every anchor is `exact`, `changed`, or `unknown`;
   `changed` and `unknown` both fail the gate.

Human review is an evidence register, not an impression. The reviewer must
state the result for each anchor and cite the comparison artifact. “Looks close”
and “recognisable” are incomplete and mean fail in exact mode.

## Prompt contract

Prompts must say that the current artwork is a literal edit/structure target,
that construction references control only the physical surface, and that all
geometry is copied through the declared transform. Prompt wording cannot
upgrade an unsupported backend or turn an unverified image into a pass.
