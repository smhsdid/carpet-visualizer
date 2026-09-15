# Backend strategies

Select one strategy from observed runtime capabilities. Keep design structure and material appearance on separate inputs whenever the backend permits it.

## Preview-only generation or editing

Use this for built-in semantic image generation and small-step edits.

```yaml
backend_strategy: preview_only
reference_budget: 3 # supporting references, excluding the design source
preferred_sequence: [material_detail, product_overview, targeted_retry]
```

Attach references in this order until the budget is full:

1. neutral macro construction reference;
2. neutral product-scale construction reference;
3. overall edge reference, exact paired mapping example, or scene reference only when the task needs that role.

When exact local motif matching matters, prepare `design_detail_crop` from the current design. It is a pattern
reference rather than a construction reference and should occupy a pattern-control slot when the backend allows
one. The deterministic design crop and current artwork control the local detail pattern; the accepted detail is the
preferred physical-texture anchor for the later overview.

Give every attachment one role. Preserve a non-square reference with neutral padding or a role-specific crop so automatic centre-cropping cannot remove its useful edge. Never stretch it.

Use the current design as the edit target. If a result fails, keep the accepted camera, design, colours, and material settings fixed and edit only the failed area or category.

For overview material QA, compare an equal-scale plain-field crop with a patterned-boundary crop. The plain field alone cannot pass material inspection. For `jacquard-01`, preserve coarse raised vertical yarns, fine horizontal cross yarns, fine recessed vertical ground/anchoring yarns, stable yarn calibre and one interlacing logic while allowing reference-supported changes in yarn exposure, coverage and relief distribution. Every yarn system follows the local artwork colour rather than a fixed pale binder colour. If two single-variable trials alternate between a smooth printed motif and enlarged rope-like, long-looped, applied, embroidered, corded or unrelated pile-like motifs while the field remains acceptable, record `pattern_material_mismatch` and stop prompt-only retries. The preview backend has reached its control ceiling for that design; route to `controllable_local` or deliver the failed preview only for diagnosis.

## Controllable local workflow

Use this when the backend exposes structure controls, independent image-reference conditioning, masks, seeds, or replayable workflow files.

```yaml
backend_strategy: controllable_local
structure_condition: [region_map, edge_map]
material_condition: ip_adapter_or_reference_branch
repair: masked_inpainting
independent_controls:
  pattern_control_scale: null
  material_ip_scale: null
  denoise_strength: null
  mask_blur_or_dilate: null
  control_guidance_start_end: null
  aspect_padding: null
seed: null
workflow_record: null
```

- Derive `region_map` from current colour regions to preserve region identity, adjacency, and negative space.
- Derive `edge_map` from the current outline and principal boundaries to preserve contour and narrow lines.
- Send neutral material references only to the material branch. Do not send them to structure controls.
- Use low-change image-to-image settings for topology preservation. More material visibility belongs in the material branch or a local mask, not in global denoising.
- Use white mask areas for edits and black areas for preservation. Edge and corner defects use a perimeter-only mask.
- Save inputs, prompts, control values, seed, output, and failure tags for every comparison. Change one independent control per experiment.

Use `detail_first` as the default for both fast material screening and pattern-sensitive work. Generate the selected
corner from the current artwork plus `design_detail_crop`, inspect it, and retain it as `material_detail_anchor` only
when its local topology and construction pass. Then generate the overview from the current artwork plus that accepted
detail anchor. The detail anchor controls texture identity, relief, interlacing and finish only; the current artwork
continues to control all overview motifs and colours. Do not use an overview to create or define the detail.

## Repair routing

| Failure tag | Targeted action |
| --- | --- |
| `pattern_drift` | Reapply the design target and strengthen region/edge structure control. Keep creativity or denoise fixed or lower. |
| `colour_leakage` | Use neutral material input and reapply colour authority inside current region masks. |
| `material_substitution` | Replace or strengthen only the material reference and physical prompt axes. |
| `construction_orientation_error` | Use the stored upright generation-input axes directly, then reapply coarse-raised vertical, fine-cross horizontal and fine-ground/anchor vertical. |
| `pattern_material_mismatch` | Separate structure and material controls; verify stable coarse-bundle calibre, fine-yarn spacing and three-system interlacing in matched pattern/field crops while retaining reference-supported jacquard exposure and relief variation. |
| `detail_camera_error` | Use a professional three-quarter macro at 25–35 degrees above the rug plane, with a diagonal leading edge, complete corner and both bound edges, shallow side raking light, and gentle far-field focus falloff while near and central interlacing stays sharp. |
| `synthetic_relief` | Rebuild only the textile surface so soft twisted coarse floats bend over horizontal yarns, compress at ties and return into the recessed ground with subtle non-repeating variation. |
| `yarn_balance_error` | Reduce coarse-crown packing, interleave larger and smaller vertical crowns, and keep horizontal fine yarns continuously exposed through plain fields, motifs and boundaries. |
| `cross_scale_inconsistency` | Reuse the accepted material-detail anchor on the overview and reduce overview texture scale while preserving the design source. |
| `edge_error` | Inpaint only the perimeter while preserving design, camera, colour, and surface. |
| `corner_mismatch` | Recreate only the detail from the declared upright-design corner, retaining its complete binding junction and adjacent motif. |
| `authority_leakage` | Remove the leaking paired, style, or quality reference. |

Do not claim ControlNet, IP-Adapter, masking, or numerical metrics unless the selected backend actually used them.
