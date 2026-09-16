# Backend strategies

Select a strategy from observed runtime capabilities. [Read the topology lock](topology-lock.md) first.

## Reference-grounded visual route

Reference-grounded image generation has references but no independent source-coordinate structure controls. It is the default route for a user-facing Wilton visual sample and records `topology_mode: approximate`. It may never claim exact topology.

For `wilton-flatweave-01` details, first compare the design hash with its paired mappings. For an exact match, attach the current design, matching paired product overview, and matching paired material detail, in that order; omit generic anchors that disagree at yarn scale or camera. Otherwise attach the complete current design first, the real detail camera-and-relief anchor second, and the multi-unit micro construction anchor third. The design alone controls outline, binding, inner lock line, motifs, colours, and every spacing relationship. The camera anchor controls focal relationship and framing; the micro anchor controls local yarn geometry. A quality anchor is optional finish evidence only and may not control geometry. Record all actual attachments and omissions.

In exact mode, record `pattern_control: unavailable`, `pattern_gate: fail`, `anchor_status: rejected`, and `failure_tags: [pattern_drift]`; return `external_execution_required` before generating the overview.

## Exact-proof route

Use deterministic `region_map` and `edge_map` inputs only to produce an aligned `structure_proof`, then run:

```text
python scripts/validate_topology.py <design_source> <structure_proof> --aligned
```

`scripts/render_wilton_calibrated.py` is proof-only: it must not emit or be presented as a material detail or product overview. A final exact textile render requires an independent material branch that both consumes a declared real construction reference and exposes structure controls; otherwise return `external_execution_required`.

## Repair routing

| Failure tag | Targeted action |
| --- | --- |
| `pattern_drift` | Rebuild the immutable structure proof and rerun the validator. |
| `pattern_material_mismatch` | Rebuild both regions with identical row cadence, bundle scale, fine threads, and relief. |
| `construction_orientation_error` | Restore product-directional bundle rows; do not rotate texture with motifs. |
| `yarn_scale_error` | Change bundle scale only; preserve pattern and camera. |
| `synthetic_relief` | Replace overlay or inflated cords with low compact bundles and shallow gaps. |
| `detail_camera_error` | Restore close oblique corner recession and both bound edges. |
| `detail_frame_cutoff` | Rebuild the continuous-plane 30-degree control; keep the far plane beyond the upper frame. |
| `camera_pattern_registration_mismatch` | Rebuild from the complete design plus declared camera anchor; preserve every original perimeter-to-pattern spacing. |
| `edge_error` | Repair only the wrapped binding and inner lock line. |
| `authority_leakage` | Remove the leaking construction or style image. |
