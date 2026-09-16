# Material configuration schema

Use visual, evidence-backed observations only. `construction` is a rendering family, not a manufacturing certification.

```yaml
material_id: wilton-flatweave-01
display_name: "Wilton Flatweave 01"
construction: wilton-flatweave
default_for_design_only: true
status: library_calibrated_visual_profile
reference_strength_default: library_grounded
render_branch: wilton_flatweave

generation_references:
  detail_camera: construction/sample-01-detail-a.jpg
  detail_micro: derived/wilton-unit-micro-anchor-v1.jpg
  overview: construction/sample-03-overall.jpg
  note: "Use the complete current design first, then the declared construction references. Avoid a paired sample whose design hash matches the current source."

derived_construction_anchors:
  unit_micro_anchor: {path: derived/wilton-unit-micro-anchor-v1.jpg, sha256: <sha256>, role: local_yarn_unit_geometry_and_spacing}
  grammar_tile: {path: derived/wilton-open-channel-grammar-tile-v1.png, role: audit_only_for_lane_stagger_and_open_channels}

paired_examples: {manifest: paired-mappings.json, count: 3, use: calibration_and_audit_only}
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
  camera_geometry: "Use the declared real lower-left camera anchor: foreground corner and larger near bundles recede across a rug plane that continues through the upper frame."
  camera_space_registration: "The complete design remains the sole geometry source: outline, binding, inner lock line, motifs, and colours retain their original relative spacing under the camera framing."
  edge_geometry: "Rounded wrapped binding plus slim inner locking line."
  fibre: unspecified
  manufacturing_process: unspecified

anti_substitutions: [smooth_print, rgb_texture_overlay, deep_pile, tall_open_loop, bead_grid, closed_equal_pitch_lattice, aligned_equal_length_rows, basket_weave, rope, raised_applique]
colour_policy: {authority_order: [explicit_colour_card, design_source], material_assets_have_colour_authority: false}
render_defaults:
  backend: reference_grounded_image_generation
  backend_strategy: unified_reference_grounded_generation
  topology_mode: strict
  pattern_control: source_guided
  surface_build_mode: yarn_geometry_or_weave_synthesis
  structure_proof_required: false
  diagnostic_proof_renderer: scripts/render_wilton_calibrated.py
  final_visual_requires: [declared_real_camera_anchor_attached, declared_real_construction_anchor_attached]
  material_reference_budget: 2
  sequence: detail_check_then_overview
  detail_corner: lower_left
  detail_camera: raking_oblique_foreground_corner_with_visible_plane_recession
  detail_camera_geometry_control: declared_real_camera_anchor
  edge_finish: wrapped_bound_edge_with_inner_lock_line
  save_generation_record: true
  generation_record_fields: [final_prompts, effective_parameters, source_sha256, ordered_reference_attachments, output_paths, evaluation_record]
```

Every manifest path must resolve. A paired mapping whose source SHA-256 matches the current design is forbidden as a generation attachment. The patterned real photo from a different paired design remains construction evidence only. The optional quality anchor controls photographic finish only and never controls current motifs, colours, yarn geometry, or camera geometry.
