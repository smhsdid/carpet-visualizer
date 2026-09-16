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
| Bundle system | Match the declared real macro's unit width, length variation, filament breakup, cross-yarn visibility, and lane staggering | Smooth capsule or bead grid, continuous ribbing, absent cross yarn, closed equal-pitch lattice, rope, basket weave, deep pile, smooth fill |
| Pattern-ground parity | All colour areas share row cadence, bundle scale, fine threads, low relief, and finish | Painted area, applied motif, or different material family |
| Yarn scale and relief | Near bundles match the declared real macro's apparent size, fuzzy multi-filament breakup, compact low crown, and shallow side shadows | Micro-grid, flattened texture, uniform tubular capsules, plastic sheen, or oversized cords |
| Edge finish | Rounded wrapped binding and slim inner lock line are continuous | Raw edge, loose fringe, missing lock line, malformed corner |
| Detail camera | Match the declared real camera anchor: complete selected corner and both edges, near foreground corner, upward-receding bound edge, visible near/far yarn-scale change, and uninterrupted carpet at the upper frame | Missing edge or corner, altered perimeter-to-pattern spacing, false horizontal far-edge cut, or camera relationship unlike the declared anchor |
| Pattern-perimeter registration | Outline, wrapped binding, inner lock line, and interior artwork retain the full design's original relative positions and spacing | Pattern, binding, or outline is independently offset, doubled, or re-spaced |
| Reference isolation | Current artwork owns all geometry and colours | Motif or palette leaks from construction reference |
| Overview framing | Complete bound rug on the declared neutral dark textile ground, all corners visible | Cropped, strongly distorted, or furnished presentation |

`topology`, `surface_build`, `bundle_system`, `pattern_ground_parity`, `edge_finish`, and `detail_camera` are hard detail gates. For an exact paired mapping, compare a 100% crop of the generated plain field, pattern boundary, and wrapped edge against its paired macro before accepting. Use `uniform_bead_grid`, `cross_yarn_missing`, `reference_geometry_mismatch`, `camera_flattening`, or `binding_overinflated` as failure tags. Any failure stops overview generation.

```yaml
evaluation_record:
  run_status: generated|external_execution_required|rejected
  topology_mode: exact|approximate
  pattern_control: deterministic|structure_branch|unavailable
  surface_build_mode: yarn_geometry_or_weave_synthesis|overlay|unavailable
  topology: pass|caveat|fail
  material: pass|caveat|fail
  bundle_system: pass|caveat|fail
  lane_spacing_and_stagger: pass|caveat|fail
  construction_orientation: pass|caveat|fail
  yarn_unit_scale: pass|caveat|fail
  relief_and_raking_camera: pass|caveat|fail
  pattern_ground_parity: pass|caveat|fail
  detail_localisation: pass|caveat|fail
  detail_texture_view: pass|caveat|fail
  camera_space_registration: pass|caveat|fail
  reference_match: pass|caveat|fail
  edge_finish: pass|caveat|fail
  failure_tags: []
```
