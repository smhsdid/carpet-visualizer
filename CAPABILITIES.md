# Rendering capabilities

Choose the strongest available rendering path and record only capabilities that the current runtime exposes.

## Capability profile

| Capability | Role in this skill | Fallback |
| --- | --- | --- |
| Image inspection | Classify reference roles and inspect generated outputs | State that visual verification is pending |
| Image generation | Produce the material detail and product overview | Return an external-execution prompt packet |
| Reference-image input | Keep artwork and construction evidence attached to the render | Restate authority and evidence in the prompt |
| Image editing | Preserve current topology from the design source | Generate from attached artwork with a stronger topology lock |
| Multiple reference images | Separate artwork, construction, style, and paired-example roles | Use only the highest-value evidence and disclose omitted inputs |
| Mask or region control | Select a representative detail boundary or edit only the perimeter | Use an explicit crop description and inspect for drift |
| Seed or replay support | Improve repeatability of a targeted retry | Preserve the full render lock and prompt instead |
| Region and edge conditioning | Preserve colour-region adjacency, negative space, contour, and narrow lines | Use the design as edit target and inspect topology visually |
| Independent material conditioning | Apply yarn, weave, scale, and finish without importing reference motifs | Use neutral construction references within the preview reference budget |
| Output condition extraction | Compare output regions or edges with the design as diagnostic signals | Use the visual quality rubric |

## Local ComfyUI capability

When `scripts/doctor.py` reports `ok: true`, the runtime has a verified local PyTorch/CUDA/ComfyUI path. Read [local ComfyUI backend](references/local-comfyui.md) before invoking it. The bundled baseline is low-denoise SDXL image-to-image and proves local execution; do not claim region control, IP-Adapter, tiled refinement, or final jacquard fidelity until a workflow actually uses and records those controls.

Use `hybrid_semantic_local` when semantic generation can establish a convincing physical product but local img2img either preserves flatness or drifts the motif. The semantic backend owns the initial physical interpretation; the local backend owns deterministic real-reference weave modulation and GPU super-resolution. Keep the original artwork as the topology and colour comparison target throughout.

## Backend record

Add this compact block to every render lock:

```yaml
render_backend: "<runtime or provider name>"
backend_strategy: preview_only|hybrid_semantic_local|controllable_local
backend_capabilities_used: [image_generation, reference_image_input]
reference_budget: 3
independent_controls: {}
consistency_contract: visual_consistency
```

Use `external_execution_required` when image generation is unavailable. This status means the prompt packet is complete but no visual output has been produced in the current environment.
