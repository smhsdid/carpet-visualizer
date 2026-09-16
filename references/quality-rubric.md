# Quality rubric

Run preflight, structure-proof, material-detail, and overview gates. Exact mode fails closed when evidence is missing.

## Preflight and proof

- Record source hash, deterministic controls, anchor register, reference roles, material manifest, and `surface_build_mode`.
- For exact mode, validate an aligned `structure_proof` before material, light, or camera rendering. A prompt or a perspective image is never proof.
- Inspect all declared construction references; state only image-supported observations.

## Output inspection

| Category | Pass condition | Fail condition |
| --- | --- | --- |
| Pattern topology | Validator passes and every anchor is exact | Any unknown or changed anchor |
| Surface build | Visible yarn geometry is rebuilt from regions | RGB artwork plus texture overlay |
| Bundle system | Short substantial bundles form stable product-directional rows, with fine interlacing visible | Bead grid, rope, basket weave, deep pile, smooth fill |
| Pattern-ground parity | All colour areas share row cadence, bundle scale, fine threads, low relief, and finish | Painted area, applied motif, or different material family |
| Yarn scale | Macro bundles remain individually legible and substantial | Micro-grid or oversized cords |
| Edge finish | Rounded wrapped binding and slim inner lock line are continuous | Raw edge, loose fringe, missing lock line, malformed corner |
| Detail camera | Complete selected corner and both edges; clear close-oblique recession | Front-on view, blur-only depth, missing edge or corner |
| Reference isolation | Current artwork owns all geometry and colours | Motif or palette leaks from construction reference |
| Overview framing | Complete bound rug on a pale floor, all corners visible | Cropped or strongly distorted rug |

`topology`, `surface_build`, `bundle_system`, `pattern_ground_parity`, `edge_finish`, and `detail_camera` are hard detail gates. Any failure stops overview generation.

```yaml
evaluation_record:
  run_status: generated|external_execution_required|rejected
  topology_mode: exact|approximate
  pattern_control: deterministic|structure_branch|unavailable
  surface_build_mode: yarn_geometry_or_weave_synthesis|overlay|unavailable
  topology: pass|caveat|fail
  material: pass|caveat|fail
  bundle_system: pass|caveat|fail
  construction_orientation: pass|caveat|fail
  yarn_unit_scale: pass|caveat|fail
  pattern_ground_parity: pass|caveat|fail
  detail_localisation: pass|caveat|fail
  detail_texture_view: pass|caveat|fail
  reference_match: pass|caveat|fail
  edge_finish: pass|caveat|fail
  failure_tags: []
```
