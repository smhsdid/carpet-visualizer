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
  detail: construction/sample-02-detail-a.jpg
  overview: construction/sample-03-overall.jpg
  note: "Attach current artwork first and exactly one real construction image second."

audit_references:
  sample_01: {overall: construction/sample-01-overall.jpg, details: [construction/sample-01-detail-a.jpg, construction/sample-01-detail-b.jpg]}
  sample_02: {overall: construction/sample-02-overall.jpg, details: [construction/sample-02-detail-a.jpg, construction/sample-02-detail-b.jpg, construction/sample-02-detail-c.jpg]}
  sample_03: {overall: construction/sample-03-overall.jpg, details: [construction/sample-03-detail-a.jpg, construction/sample-03-detail-b.jpg]}

construction_lock:
  surface_structure: "Aligned rows of short substantial multi-filament bundles with finer visible interlacing threads."
  organisation: "Bundle rows follow the upright rug long axis; fine threads cross and separate rows."
  pattern_formation: "All current colours are yarn-built inside the same system."
  relief: "Compact low crowns, shallow gaps, restrained filament highlights."
  edge_geometry: "Rounded wrapped binding plus slim inner locking line."
  fibre: unspecified
  manufacturing_process: unspecified

anti_substitutions: [smooth_print, rgb_texture_overlay, deep_pile, tall_open_loop, bead_grid, basket_weave, rope, raised_applique]
colour_policy: {authority_order: [explicit_colour_card, design_source], material_assets_have_colour_authority: false}
render_defaults:
  topology_mode: exact
  surface_build_mode: yarn_geometry_or_weave_synthesis
  material_reference_budget: 1
  sequence: detail_gate_then_overview
  detail_corner: lower_left
  edge_finish: wrapped_bound_edge_with_inner_lock_line
```

Every manifest path must resolve. A patterned real photo may be used as one secondary construction reference only; it never controls the current design.
