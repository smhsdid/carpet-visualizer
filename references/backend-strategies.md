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

Give every attachment one role. Preserve a non-square reference with neutral padding or a role-specific crop so automatic centre-cropping cannot remove its useful edge. Never stretch it.

Use the current design as the edit target. If a result fails, keep the accepted camera, design, colours, and material settings fixed and edit only the failed area or category.

For overview material QA, compare an equal-scale plain-field crop with a patterned-boundary crop. The plain field alone cannot pass material inspection. For `jacquard-01`, preserve coarse raised vertical yarns, fine horizontal cross yarns, fine recessed vertical ground/anchoring yarns, stable yarn calibre and one interlacing logic while allowing reference-supported changes in yarn exposure, coverage and relief distribution. Every yarn system follows the local artwork colour rather than a fixed pale binder colour. If two single-variable trials alternate between a smooth printed motif and enlarged rope-like, long-looped, applied, embroidered, corded or unrelated pile-like motifs while the field remains acceptable, record `pattern_material_mismatch` and stop prompt-only retries. The preview backend has reached its control ceiling for that design; route to `controllable_local` or deliver the failed preview only for diagnosis.

## Hybrid semantic and local workflow

Use `hybrid_semantic_local` after two controlled local img2img trials demonstrate the local model's control ceiling: one remains flat and the other introduces motif drift, material substitution, or unrelated ornament.

1. Generate a semantic overview master using the current design as strict topology and colour authority plus the selected real macro, product-scale, and overall construction references. Do not use an AI sample as construction evidence.
2. Reject the master before local processing if motif count, adjacency, outline, orientation, or colour-region ownership changed.
3. Run `scripts/run-hybrid-postprocess.ps1` on the accepted master. It injects only grayscale high-frequency relief extracted from the bundled real construction photos, then uses the pinned local super-resolution model on the GPU.
4. Inspect the final result at full frame and at 100% crops from the centre field and a patterned boundary. Reject obvious mirrored tiling, haloed edges, synthetic bead noise, background texture, or a different weave family between regions.

Record the semantic backend, its exact reference roles and prompt separately from the local model hashes, weave parameters, scale factor, and ComfyUI prompt ID. Local enhancement cannot repair a structurally incorrect semantic master.

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

For fast material screening, `detail_first` remains valid. Anchor it to the selected corner in the upright design coordinate frame. For strict cross-scale consistency, use `overview_first`, then crop the selected overview corner and locally inpaint that crop into a detail so both views share location, product identity, edge construction, and texture hierarchy.

## Repair routing

| Failure tag | Targeted action |
| --- | --- |
| `pattern_drift` | Reapply the design target and strengthen region/edge structure control. Keep creativity or denoise fixed or lower. |
| `colour_leakage` | Use neutral material input and reapply colour authority inside current region masks. |
| `material_substitution` | Replace or strengthen only the material reference and physical prompt axes. |
| `construction_orientation_error` | Use the stored upright generation-input axes directly, then reapply coarse-raised vertical, fine-cross horizontal and fine-ground/anchor vertical. |
| `pattern_material_mismatch` | Separate structure and material controls; verify stable coarse-bundle calibre, fine-yarn spacing and three-system interlacing in matched pattern/field crops while retaining reference-supported jacquard exposure and relief variation. |
| `detail_camera_error` | Move the lens nearly level with the near binding to 8–12 degrees above the rug plane; require a prominent binding side face, strong depth recession, near-to-far scale compression, and gentle far-field focus falloff while near and central interlacing stays sharp. |
| `synthetic_relief` | Rebuild only the textile surface so soft twisted coarse floats bend over horizontal yarns, compress at ties and return into the recessed ground with subtle non-repeating variation. |
| `yarn_balance_error` | Reduce coarse-crown packing, interleave larger and smaller vertical crowns, and keep horizontal fine yarns continuously exposed through plain fields, motifs and boundaries. |
| `cross_scale_inconsistency` | Reuse the accepted anchor and reduce overview texture scale, or derive detail from the accepted overview. |
| `edge_error` | Inpaint only the perimeter while preserving design, camera, colour, and surface. |
| `corner_mismatch` | Recreate only the detail from the declared upright-design corner, retaining its complete binding junction and adjacent motif. |
| `authority_leakage` | Remove the leaking paired, style, or quality reference. |

Do not claim ControlNet, IP-Adapter, masking, or numerical metrics unless the selected backend actually used them.
