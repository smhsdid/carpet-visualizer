# Rendering capabilities

Choose the strongest available rendering path and record only capabilities that the current runtime exposes.

## Capability profile

| Capability | Role in this skill | Fallback |
| --- | --- | --- |
| Image inspection | Classify reference roles and inspect generated outputs | State that visual verification is pending |
| Image generation | Produce the material detail and product overview | Return an external-execution prompt packet |
| Reference-image input | Supply visual context | Never treat it as topology control; prompts cannot compensate |
| Image editing | Preserve current topology only when the backend exposes a real structure-preserving edit path and can emit an aligned proof | Treat as unsupported for exact mode |
| Multiple reference images | Separate artwork, construction, style, and paired-example roles | Use only the highest-value evidence and disclose omitted inputs |
| Mask or region control | Supply exact structure controls or a scoped repair mask | Exact mode fails when these controls are absent |
| Seed or replay support | Improve repeatability of a targeted retry | Preserve the full render lock and prompt instead |
| Region and edge conditioning | Supply the structure branch's exact region and boundary controls | Exact mode fails when these controls are absent |
| Independent material conditioning | Reconstruct visible coloured yarn units, weave, scale, relief, and finish without importing reference motifs | A luminance-only or generic texture overlay fails the material gate; use neutral construction references within the preview reference budget |
| Output condition extraction | Produce an aligned `structure_proof` and measurable region/boundary evidence | Exact mode fails closed when proof evidence is absent |

## Backend record

Add this compact block to every render lock:

```yaml
render_backend: "<runtime or provider name>"
backend_strategy: reference_grounded_visual|structure_proof_only|controllable_local
backend_capabilities_used: [image_generation, reference_image_input]
reference_budget: 2 # accepted quality anchor plus one real multi-unit construction anchor
topology_mode: exact|approximate
pattern_control: deterministic|structure_branch|unavailable
surface_build_mode: yarn_geometry_or_weave_synthesis|overlay|unavailable
structure_proof: <path-or-null>
topology_verification: automated_aligned|anchor_register|unavailable
independent_controls: {}
consistency_contract: visual_consistency
```

`reference_grounded_visual` means semantic generation with the complete current design, a recorded real detail-camera anchor, a recorded accepted quality anchor, and one recorded real multi-unit micro construction anchor. It has no independent structure controls. The complete design remains the only source of pattern and spacing; the camera anchor supplies focal relationship and framing only. It is a user-facing `topology_mode: approximate` visual route, never an exact claim. `structure_proof_only` means a deterministic source-coordinate proof with no material-detail or overview deliverable. In exact mode without an independent material branch, record `pattern_control: unavailable`, fail the pattern gate, and return `external_execution_required`. Regardless of topology mode, a Wilton flatweave output whose `surface_build_mode` is `overlay` fails the material gate because the source artwork remains a flat visible plate.

Use `external_execution_required` when image generation is unavailable or when exact topology control is unavailable. This status means the prompt packet is complete but no compliant visual output has been produced in the current environment.
