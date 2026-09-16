# Rendering capabilities

Choose the strongest image capability exposed by the current runtime, but keep one user-facing generation flow. The artwork remains the pattern and colour authority; references provide construction and presentation evidence only.

## Capability profile

| Capability | Role in this skill | Fallback |
| --- | --- | --- |
| Image inspection | Classify references and run the lightweight output check | Record that visual inspection is pending |
| Image generation | Produce the material detail and product overview | Return an external-execution prompt packet |
| Reference-image input | Supply camera, construction, and finish context | Use the highest-value declared references and record omissions |
| Image editing | Preserve current topology when the backend exposes useful structure-preserving controls | Use the unified reference-grounded generation flow |
| Multiple reference images | Separate artwork, construction, style, and paired-example roles | Use the highest-value evidence and disclose omitted inputs |
| Mask or region control | Improve pattern preservation or scope a repair | Continue with source-guided generation and record the limitation |
| Seed or replay support | Improve repeatability | Save all available parameters and prompts |
| Region and edge conditioning | Improve outline, boundary, and spacing preservation | Keep the complete current design attached |
| Independent material conditioning | Reconstruct visible coloured yarn units, weave, scale, relief, and finish without importing reference motifs | Use neutral construction references; a flat overlay fails the material check |
| Output condition extraction | Support lightweight inspection and evidence capture | Record manual inspection status |

## Backend record

Add this compact block to every render lock:

```yaml
render_backend: "<runtime or provider name>"
backend_strategy: unified_reference_grounded_generation|diagnostic_structure_proof|external_execution
backend_capabilities_used: [image_generation, reference_image_input]
reference_budget: 2 # camera/construction anchor plus one multi-unit construction anchor
topology_mode: strict # internal run label: preserve the source pattern as strictly as possible
pattern_control: source_guided|structure_branch|unavailable
surface_build_mode: yarn_geometry_or_weave_synthesis|overlay|unavailable
structure_proof: <path-or-null>
topology_verification: diagnostic_only|unavailable
independent_controls: {}
consistency_contract: visual_consistency
final_prompts:
  detail: <path-or-inline-text>
  overview: <path-or-inline-text>
generation_parameters: {}
```

`unified_reference_grounded_generation` means the complete current design is attached first, followed by the declared construction references. It is always used for the user-facing detail and overview. The fixed lower-left detail is generated first; a lightweight check is recorded; the overview is then generated automatically. Reference input supports pattern preservation but is not itself a mathematical guarantee.

The deterministic helper may create source-coordinate controls or a diagnostic structure proof, but it is not a final textile renderer and its result is not a user-facing image. If image generation is unavailable, return `external_execution_required` with the completed prompts, effective parameters, ordered attachments, and run record.

Regardless of backend, a Wilton flatweave output whose `surface_build_mode` is `overlay` fails the material check because the source artwork remains a flat visible plate.
