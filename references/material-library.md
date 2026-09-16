# Material library

The packaged library lets a later conversation generate from artwork alone. Each material entry contains a manifest and only durable, useful assets.

## Authority matrix

| Input | Controls | Must never control |
| --- | --- | --- |
| Current `design_source` | Current outline, motif topology, placement, negative space, default colours | Material construction |
| Explicit mapped `colour_card` | Mapped current colour regions | Pattern geometry or material structure |
| `macro_detail` construction reference | Yarn geometry, interlacing, local relief | Current motifs or colours |
| `product_scale_crop` construction reference | Density, spacing, hierarchy, grain | Current motifs or colours |
| `overall_product` construction reference | Approximate product scale, thickness, binding | Current motifs or colours |
| `paired_mapping_example` | Historical design-to-physical translation for the same construction | Current motif identity, layout, or colours |
| `scene_style_reference` | Camera, lighting, background, crop, presentation | Pattern, colour, or construction |
| `quality_anchor` | Secondary polish target | Any fact contradicted by real evidence |

## Current library

`structured-woven-surface-01` is the default design-only material. Read its [manifest](../assets/material-library/structured-woven-surface-01/manifest.yaml) and follow [the structured woven surface branch](structured-woven-surface-branch.md).

For this material, an exact run requires a structure-proof path before any material generation. The current design retains exclusive pattern and colour authority. One declared real construction reference has high priority for the observed yarn-bundle system, fine interlacing, relief, edge, and close-oblique camera or product-scale presentation, but must never contribute its motif or colours. Multi-reference input does not provide structure control; if the backend cannot emit an aligned proof, record `pattern_control: unavailable`, fail the pattern gate, and return `external_execution_required`.

## Adding a paired mapping example

A valid pair requires all three files from the same physical sample:

1. `paired_design_source`: the exact design sent to sampling;
2. `paired_product_overview`: the corresponding complete physical product;
3. `paired_material_detail`: a sharp detail of that same product.

Record one `pair_id`, one `material_id`, and `design_match: exact`. If the original artwork is missing, uncertain, revised after sampling, or belongs to another product, do not classify the photos as a paired example. Keep them as construction or scene references instead.

Recommended future layout:

```text
assets/material-library/<material-id>/
  manifest.yaml
  construction/
  derived/
  paired-examples/<pair-id>/
    design-source.<ext>
    product-overview.<ext>
    material-detail.<ext>
  style/
```

Do not add empty placeholder directories or fabricated reference images.
