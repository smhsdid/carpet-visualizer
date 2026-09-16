# Backend strategies

Select a strategy from observed runtime capabilities. [Read the topology lock](topology-lock.md) first.

## Preview-only generation or editing

Preview-only image generation has references but no independent source-coordinate structure controls. It is valid only when the user explicitly accepts `topology_mode: approximate`.

For `structured-woven-surface-01`, attach current artwork first and exactly one manifest-declared real construction image second. The second image controls only the aligned short-bundle rows, fine interlacing visibility, compact relief, bound edge, and camera. Do not attach other patterned samples or a prior generated image. Record `reference_limited: true` when multi-reference input is unavailable.

In exact mode, record `pattern_control: unavailable`, `pattern_gate: fail`, `anchor_status: rejected`, and `failure_tags: [pattern_drift]`; return `external_execution_required` before generating the overview.

## Controllable local workflow

Use deterministic `region_map` and `edge_map` inputs for the structure branch. Produce an aligned `structure_proof` from those controls only and run:

```text
python scripts/validate_topology.py <design_source> <structure_proof> --aligned
```

Only after it passes, send one real construction image to an independent material branch. The branch reconstructs aligned short multi-filament bundle rows, visible fine interlacing threads, shallow gaps, low crowns, and restrained filament highlights. It must not leave the source RGB image visible and add a texture effect; record that path as `surface_build_mode: overlay` and reject it.

Generate detail first. Compare equal-scale plain-field and patterned-boundary crops at 100%, then generate overview only after every hard gate passes.

## Repair routing

| Failure tag | Targeted action |
| --- | --- |
| `pattern_drift` | Rebuild the immutable structure proof and rerun the validator. |
| `pattern_material_mismatch` | Rebuild both regions with identical row cadence, bundle scale, fine threads, and relief. |
| `construction_orientation_error` | Restore product-directional bundle rows; do not rotate texture with motifs. |
| `yarn_scale_error` | Change bundle scale only; preserve pattern and camera. |
| `synthetic_relief` | Replace overlay or inflated cords with low compact bundles and shallow gaps. |
| `detail_camera_error` | Restore close oblique corner recession and both bound edges. |
| `edge_error` | Repair only the wrapped binding and inner lock line. |
| `authority_leakage` | Remove the leaking construction or style image. |
