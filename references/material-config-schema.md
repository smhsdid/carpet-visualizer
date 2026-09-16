# Material configuration schema

Use visual, evidence-backed observations only. `construction` is a rendering family, not a manufacturing certification.

```yaml
material_id: wilton-flatweave-01
display_name: "Wilton Flatweave 01"
construction: wilton-flatweave
default_for_design_only: true
status: task_reference_grounded_user_confirmed_visual_profile
reference_strength_default: task_reference_grounded
render_branch: wilton_flatweave

generation_references:
  detail: derived/wilton-unit-micro-anchor-v1.jpg
  overview: derived/wilton-unit-micro-anchor-v1.jpg
  note: "A detail attaches current design, a generic camera-and-construction anchor from another paired design, and a generic micro construction anchor. A matching pair is calibration evidence only and cannot be attached."

derived_construction_anchors:
  unit_micro_anchor: {path: derived/wilton-unit-micro-anchor-v1.jpg, sha256: <sha256>, role: exact_local_yarn_unit_geometry_and_spacing}
  grammar_tile: {path: derived/wilton-open-channel-grammar-tile-v1.png, role: audit_only_for_lane_stagger_and_open_channels}

audit_references:
  sample_01: {overall: construction/sample-01-overall.jpg, details: [construction/sample-01-detail-a.jpg, construction/sample-01-detail-b.jpg]}
  sample_02: {overall: construction/sample-02-overall.jpg, details: [construction/sample-02-detail-a.jpg, construction/sample-02-detail-b.jpg, construction/sample-02-detail-c.jpg]}
  sample_03: {overall: construction/sample-03-overall.jpg, details: [construction/sample-03-detail-a.jpg, construction/sample-03-detail-b.jpg]}

paired_examples: {manifest: paired-mappings.json, count: 3, use: calibration_and_leave_one_out_review}
quality_anchor:
  path: quality/accepted-detail-anchor-v1.png
  sha256: <sha256>
  role: accepted_wilton_detail_polish
  controls: [exposure, white_balance, product_photography]
  does_not_control: [current_motifs, current_colours, current_layout, yarn_geometry, camera_geometry, manufacturing_specification]

construction_lock:
  surface_structure: "Short-and-long substantial multi-filament bundles occupy product-directional lanes with open shadowed longitudinal channels and finer visible interlacing threads."
  organisation: "Bundle lanes follow the upright rug long axis; adjacent lanes stagger their bundle ends while fine threads cross and separate the open channels."
  bundle_length_variation: "Visibly short and longer tapered units occur in every near-detail area of every colour region."
  two_length_classes: "Both unit lengths remain visibly present; their alternation is irregular."
  longitudinal_channels: "Open close-detail channels expose finer cross yarns between bundle lanes."
  pattern_formation: "All current colours are yarn-built inside the same system."
  relief: "Coarse compact low crowns with visibly raised middles and shallow side shadows from a raking camera."
  camera_geometry: "Approximately 30-degree raking camera: foreground corner and larger near bundles recede across a rug plane that continues through the upper frame."
  camera_space_registration: "The complete design remains the sole geometry source: outline, binding, inner lock line, motifs, and colours retain their original relative spacing under the camera-anchor framing."
  edge_geometry: "Rounded wrapped binding plus slim inner locking line."
  fibre: unspecified
  manufacturing_process: unspecified

anti_substitutions: [smooth_print, rgb_texture_overlay, deep_pile, tall_open_loop, bead_grid, closed_equal_pitch_lattice, aligned_equal_length_rows, basket_weave, rope, raised_applique]
colour_policy: {authority_order: [explicit_colour_card, design_source], material_assets_have_colour_authority: false}
render_defaults:
  backend: reference_grounded_image_generation
  backend_strategy: reference_grounded_visual_preview
  topology_mode: approximate
  exact_proof_renderer: scripts/render_wilton_calibrated.py
  exact_proof_renderer_role: structure_proof_only
  final_visual_requires: [declared_real_camera_anchor_attached, declared_real_construction_anchor_attached]
  surface_build_mode: yarn_geometry_or_weave_synthesis
  material_reference_budget: 2
  sequence: detail_gate_then_overview
  detail_corner: lower_left
  detail_camera: raking_oblique_foreground_corner_with_visible_plane_recession
  detail_camera_geometry_control: declared_real_camera_anchor
  edge_finish: wrapped_bound_edge_with_inner_lock_line
```

Every manifest path must resolve. A paired mapping whose source SHA-256 matches the current design is forbidden as a generation attachment. The patterned real photo from a different paired design remains the construction reference; the accepted quality anchor is optional visual-finish evidence only. Neither controls the current design.
