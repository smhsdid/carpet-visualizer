# Backend strategy

## Unified reference-grounded generation

Use one route for every design, regardless of artwork complexity. Attach the complete current design first, then the declared construction references. Keep the fixed lower-left detail. Generate the detail first, record a lightweight check, and automatically generate the overview.

The current design controls the outline, binding, inner lock line, motifs, colours, spacing, and all pattern relationships. The camera reference controls framing and recession. The multi-unit construction reference controls local yarn geometry, exposed cross yarn, bundle size, and gap proportion. An optional quality anchor controls photographic finish only.

Reference images help the model preserve the design but do not constitute a mathematical proof. Any visual drift is recorded as a caveat in the run record; it does not create a second generation route or require user confirmation.

## Diagnostic controls

Use deterministic source-coordinate controls when the design is a local raster. They provide a stable source hash, region information, edge information, and an audit snapshot. A diagnostic structure proof may be generated for troubleshooting, but it is not a final material-detail image and is not a prerequisite for the unified visual route.

## Failure and repair routing

Stop only when the image backend is unavailable, an output is missing or unreadable, or the generated file is technically invalid. For visual problems, record the failure tag and continue to the overview unless the user later requests a targeted retry.

| Failure tag | Targeted action |
| --- | --- |
| `pattern_drift` | Rebuild from the complete current design and preserve the source hash. |
| `pattern_material_mismatch` | Rebuild both regions with identical lane cadence, bundle scale, fine threads, and relief. |
| `construction_orientation_error` | Restore product-directional bundle rows; do not rotate texture with motifs. |
| `yarn_scale_error` | Change bundle scale only; preserve pattern and camera. |
| `synthetic_relief` | Replace overlay or inflated cords with low compact bundles and shallow gaps. |
| `detail_camera_error` | Restore the fixed lower-left close-oblique corner framing and both bound edges. |
| `detail_frame_cutoff` | Keep the upper frame within continuous rug surface. |
| `camera_pattern_registration_mismatch` | Rebuild from the complete design and preserve every original perimeter-to-pattern spacing. |
| `edge_error` | Repair only the wrapped binding and inner lock line. |
| `authority_leakage` | Remove the leaking construction or style image. |

Always save the final prompts, effective parameters, ordered reference attachments, source hash, outputs, and check results in the run record.
