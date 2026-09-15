# Material config schema

Use this YAML shape for a reusable material-library entry. Store only visual facts supported by references or explicit user input. Leave unknown manufacturing facts unset.

```yaml
material_id: company-jacquard-01
display_name: "Company jacquard 01"
construction: jacquard
default_for_design_only: false
status: construction_calibrated
reference_strength_default: library_grounded
render_branch: standard_reference_jacquard

standard_texture_references:
  detail:
    file: derived/jacquard-standard-detail-neutral.png
    controls: [fine_surface, interlacing, local_relief]
    must_not_control: [current_artwork, current_colours, scene]
  overview:
    file: derived/jacquard-standard-overview-neutral.png
    controls: [product_scale, density, direction, edge_family]
    must_not_control: [current_artwork, current_colours, scene]

construction_references:
  macro_detail:
    original: construction/macro-detail.jpg
    controls: [yarn_geometry, interlacing, local_relief]
    must_not_control: [current_artwork, current_colours]
  product_scale_crop: null
  overall_product: null

paired_examples: []
scene_style_reference: null
quality_anchor: null

construction_lock:
  orientation_frame: "Describe the upright finished-product coordinate frame."
  coarse_raised_yarn_axis: "Describe the coarse raised-yarn direction after reference-orientation normalisation."
  fine_cross_yarn_axis: "Describe the finer crossing-yarn direction after reference-orientation normalisation."
  fine_ground_anchor_axis: "Describe the recessed fine ground or anchoring-yarn direction."
  surface_structure: "Describe observed construction."
  yarn_geometry: "Describe observed yarn geometry."
  interlacing: "Describe observed interlacing."
  grain_direction: "Describe observed grain."
  scale_behavior: "Describe what is visible in macro and how it compresses at product distance."
  surface_relief: "Describe observed relief hierarchy."
  yarn_exposure_balance: "Describe the visible share of dominant and supporting yarn systems across plain and patterned regions."
  boundary_behavior: "Describe how the same construction continues across colour changes."
  yarn_colour_behavior: "Describe how every yarn system inherits local design-source colours."
  edge_geometry: "Describe observed edge or use default."
  finish: "Describe only observed roughness, matte or sheen, fuzz, and directional light response."

anti_substitutions: []

reference_orientation_notes:
  overall_product: "Declare folding, mirroring or sideways photography that changes apparent image axes."
  normalisation: "Describe how reference directions map into upright finished-product coordinates."

colour_policy:
  authority_order: [explicit_colour_card, design_source]
  material_assets_have_colour_authority: false

render_defaults:
  backend: runtime_default
  backend_strategy: preview_only
  reference_budget: 2
  sequence: overview_first_then_detail_from_overview_anchor
  detail_anchor_mode: overview_derived_corner_context
  pattern_anchor_mode: design_crop_plus_overview_anchor
  detail_corner: lower_left
  detail_orientation: upright_design_source
  detail_context: [corner_junction, two_bound_edges, adjacent_border_motif, colour_boundary]
  edge_finish: serged_overlock
  detail_target: null
  detail_view: professional_three_quarter_macro_25_35_degrees_above_plane
  detail_frame_coverage: "96–98% rug surface, complete near corner junction and short segments of both bound edges visible"
  detail_camera_evidence: "Near binding side face is prominent; depth recession and near-to-far scale compression are visible; near and central interlacing stays sharp with gentle far-field focus falloff."
  overview_view: standing_observer_restrained_near_overhead_sample_shot
  overview_frame_coverage: "92–96%, complete bound outline visible with narrow quiet floor margins"
  photography_style: bright_crisp_commercial_product
  presentation_tone: "high-key clean exposure, luminous whites, clear colours, medium-high contrast"
  overview_background: subtle_pale_floor_or_porcelain_tile_with_soft_contact_shadow

confidence:
  level: reference_based
  notes: "State missing reference roles or uncertain observations."

known_failure_modes: []
```

## Per-run render lock

```yaml
design_source: "current attached artwork"
material_id: jacquard-01
construction: jacquard
render_branch: standard_reference_jacquard
reference_strength: library_grounded
standard_texture_references: [detail, overview]
material_reference_mode: standard_texture_references
mapping_reference_mode: none
construction_lock:
  orientation_frame: upright_design_source
  coarse_raised_yarn_axis: "..."
  fine_cross_yarn_axis: "..."
  fine_ground_anchor_axis: "..."
  surface_structure: "..."
  yarn_geometry: "..."
  interlacing: "..."
  grain_direction: "..."
  scale_behavior: "..."
  surface_relief: "..."
  yarn_exposure_balance: "..."
  boundary_behavior: "..."
  yarn_colour_behavior: "..."
  edge_geometry: "..."
  finish: "..."
anti_substitutions: []
colour_authority: design_source
colour_mapping: []
photography_style: bright_crisp_commercial_product
presentation_tone: "high-key clean exposure, luminous whites, clear colours, medium-high contrast; no grey veil or subdued grading"
edge_finish: serged_overlock
detail_anchor_mode: overview_derived_corner_context
pattern_anchor_mode: design_crop_plus_overview_anchor
detail_corner: lower_left
detail_orientation: upright_design_source
detail_context: [corner_junction, two_bound_edges, adjacent_border_motif, colour_boundary]
detail_camera_lock: "professional three-quarter macro, camera 25–35 degrees above rug plane, diagonal leading edge, complete corner and both bound edges, near and central interlacing sharp, gentle far-field focus falloff"
overview_camera_lock: "standing-observer downward sample shot with restrained near-overhead angle, slightly closer framing, mild near-to-far perspective with the near lower edge only slightly larger than the far upper edge, rug square to frame with long axis vertical and 0–2 degrees residual rotation, 92–96% frame coverage, complete outline visible"
render_backend: runtime_default
backend_strategy: preview_only
backend_capabilities_used: [image_generation, reference_image_input]
reference_budget: 3
independent_controls: {}
render_sequence: overview_first_then_detail_from_overview_anchor
deliverables: [material_detail, product_overview]
consistency_contract: visual_consistency
evaluation_record:
  topology: pass|caveat|fail
  material: pass|caveat|fail
  construction_orientation: pass|caveat|fail
  pattern_ground_parity: pass|caveat|fail
  detail_localisation: pass|caveat|fail
  detail_texture_view: pass|caveat|fail
  overview_framing: pass|caveat|fail
  presentation_tone: pass|caveat|fail
  relief_lustre: pass|caveat|fail
  cross_scale_consistency: pass|caveat|fail
  colour_authority: pass|caveat|fail
  edge_finish: pass|caveat|fail
  region_iou: null
  boundary_f_score: null
  colour_delta_e: null
  failure_tags: []
```

`render_backend` is the actual runtime or provider name. `runtime_default` is valid only before a backend is selected. See [rendering capabilities](../CAPABILITIES.md) for capability recording and fallback behaviour.

## Reference strength and confidence

| Evidence | `reference_strength` | Confidence label |
| --- | --- | --- |
| Task-specific real material photo | `task_reference_grounded` | `reference_based` |
| Bundled real material entry | `library_grounded` | `reference_based` |
| Generic profile only | `profile_only` | `provisional` |

If references conflict, use the user-declared role and higher-precedence evidence. Do not average incompatible constructions.
