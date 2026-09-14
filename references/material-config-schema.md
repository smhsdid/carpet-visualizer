# Material config schema

Use this YAML shape for a reusable material-library entry. Store only visual facts supported by references or explicit user input. Leave unknown manufacturing facts unset.

```yaml
material_id: company-jacquard-01
display_name: "Company jacquard 01"
construction: jacquard
default_for_design_only: false
status: construction_calibrated
reference_strength_default: library_grounded

construction_references:
  macro_detail:
    original: construction/macro-detail.jpg
    generation_input: derived/macro-detail-neutral.jpg
    controls: [yarn_geometry, interlacing, local_relief]
    must_not_control: [current_artwork, current_colours]
  product_scale_crop: null
  overall_product: null

paired_examples: []
scene_style_reference: null
quality_anchor: null

construction_lock:
  surface_structure: "Describe observed construction."
  yarn_geometry: "Describe observed yarn geometry."
  interlacing: "Describe observed interlacing."
  grain_direction: "Describe observed grain."
  surface_relief: "Describe observed relief hierarchy."
  edge_geometry: "Describe observed edge or use default."
  finish: "Describe only observed matte, sheen, fuzz, or directional effects."

colour_policy:
  authority_order: [explicit_colour_card, design_source]
  material_assets_have_colour_authority: false

render_defaults:
  backend: runtime_default
  sequence: detail_first
  detail_region: representative_boundary
  edge_finish: serged_overlock
  overview_view: gently_oblique_product_photo

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
reference_strength: library_grounded
material_reference_mode: bundled_neutral_construction_references
mapping_reference_mode: none
construction_lock:
  surface_structure: "..."
  yarn_geometry: "..."
  interlacing: "..."
  grain_direction: "..."
  surface_relief: "..."
  edge_geometry: "..."
  finish: "..."
colour_authority: design_source
colour_mapping: []
photography_style: default_neutral_product
edge_finish: serged_overlock
camera_lock: "20–30 degree downward view, natural perspective, near edge visible"
render_backend: runtime_default
backend_capabilities_used: [image_generation, reference_image_input]
render_sequence: detail_first
deliverables: [material_detail, product_overview]
consistency_contract: visual_consistency
```

`render_backend` is the actual runtime or provider name. `runtime_default` is valid only before a backend is selected. See [rendering capabilities](../CAPABILITIES.md) for capability recording and fallback behaviour.

## Reference strength and confidence

| Evidence | `reference_strength` | Confidence label |
| --- | --- | --- |
| Task-specific real material photo | `task_reference_grounded` | `reference_based` |
| Bundled real material entry | `library_grounded` | `reference_based` |
| Generic profile only | `profile_only` | `provisional` |

If references conflict, use the user-declared role and higher-precedence evidence. Do not average incompatible constructions.
