# Quality rubric

Run preflight, material-detail, and overview checks in one continuous flow. The check is lightweight and diagnostic: it records visible problems, but it does not wait for user approval.

## Preflight

- Record source hash, deterministic controls, anchor register, reference roles, material manifest, and `surface_build_mode`.
- Inspect all declared construction references and state only image-supported observations.
- Save the final prompts and effective generation parameters before the generation call.

## Detail check

| Category | Pass condition | Caveat or fail condition |
| --- | --- | --- |
| Pattern preservation | Current outline, motifs, boundaries, spacing, and colour relationships remain recognisable and registered | Visible drift, missing motif, changed spacing, or imported reference pattern |
| Surface build | Visible yarn geometry is rebuilt from source regions | RGB artwork plus texture overlay |
| Bundle system | Short and longer units, filament breakup, cross-yarn visibility, and lane staggering are visible | Smooth fill, bead grid, continuous ribbing, absent cross yarn, closed lattice, rope, basket weave, or deep pile |
| Pattern-ground parity | Ground, motif, and boundary share row cadence, bundle scale, fine threads, low relief, and finish | Painted area, applied motif, or different material family |
| Yarn scale and relief | Near bundles show compact low crowns and shallow side shadows | Flattened texture, plastic sheen, or oversized cords |
| Edge finish | Rounded wrapped binding and slim inner lock line are continuous | Raw edge, loose fringe, missing lock line, or malformed corner |
| Detail camera | Lower-left corner and both bound edges are visible; the surface recedes and continues through the upper frame | Missing edge or corner, false horizontal far edge, or flattened view |
| Pattern-perimeter registration | Outline, binding, inner lock line, and interior artwork retain their relative positions | Pattern, binding, or outline is independently offset or re-spaced |
| Reference isolation | Current artwork owns all geometry and colours | Motif or palette leaks from a construction reference |

## Overview check

Confirm that the complete bound rug is visible on the declared neutral dark textile ground, all four corners are present, the same construction family is used, and no furnishings, text, or watermark were introduced.

## Run record schema

```yaml
evaluation_record:
  run_status: generated|external_execution_required|rejected
  topology_mode: strict
  pattern_control: source_guided|structure_branch|unavailable
  surface_build_mode: yarn_geometry_or_weave_synthesis|overlay|unavailable
  pattern_preservation: pass|caveat|fail
  surface_build: pass|caveat|fail
  bundle_system: pass|caveat|fail
  lane_spacing_and_stagger: pass|caveat|fail
  construction_orientation: pass|caveat|fail
  yarn_unit_scale: pass|caveat|fail
  relief_and_raking_camera: pass|caveat|fail
  pattern_ground_parity: pass|caveat|fail
  detail_localisation: pass|caveat|fail
  detail_texture_view: pass|caveat|fail
  pattern_perimeter_registration: pass|caveat|fail
  reference_isolation: pass|caveat|fail
  overview_framing: pass|caveat|fail
  presentation_tone: pass|caveat|fail
  cross_scale_consistency: pass|caveat|fail
  colour_authority: pass|caveat|fail
  edge_finish: pass|caveat|fail
  failure_tags: []
```

Only a missing, unreadable, or technically invalid output stops the automatic overview step. Visual issues are retained as caveats or failure tags for later targeted retries.
