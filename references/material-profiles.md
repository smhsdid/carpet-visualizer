# Material profiles

These profiles control visual construction only. Task-specific real material photos override a bundled material entry; a bundled entry overrides generic traits. Colours come from an explicit mapped colour card or, by default, the current design source.

## Construction-reference roles

| Role | Useful image | Authority |
| --- | --- | --- |
| `macro_detail` | Close, sharp view of yarns, loops, cut ends, or weave | Yarn geometry, interlacing, local relief |
| `product_scale_crop` | Larger surface area at a normal close-product distance | Texture density, spacing, hierarchy |
| `overall_product` | Whole product plus one visible edge or corner | Approximate thickness, binding, whole-product scale |

Use neutral or soft directional light, visible focus, and minimal perspective distortion. Strong filters, coloured lighting, extreme blur, or multiple constructions in one crop weaken evidence. A single useful photo is allowed; disclose its limited authority instead of inventing missing facts.

## `printed-low-pile`

- Surface: level, closely packed, low matte pile with colour carried in the fibres.
- Boundary: graphic regions remain clear with slight fibre softness and no structural relief.
- Default status without photos: `profile_only`, `provisional`.
- Failure signatures: woven grid, raised motifs, deep pile, embossed channels.

## `flatwoven`

- Surface: low-profile, matte warp-and-weft interlacing with restrained yarn irregularity and very low relief.
- Boundary: colour regions read as part of one woven plane; fine design lines remain recognisable.
- Scale: individual yarns are visible in the detail but compress into a coherent textile at overview distance.
- Default status without photos: `profile_only`, `provisional`.
- Failure signatures: plush pile, fur, oversized threads, basket-like blocks, printed smoothness.

## `jacquard`

When only a design is uploaded, use bundled `jacquard-01`. Open its manifest and inspect its neutral generation inputs. Use the originals for audit or closer human inspection, not as the default palette-bearing generation inputs.

For any calibrated pack, use each scale separately:

- `macro_detail`: yarn shape, twist, fuzz, interlacing, and local transition.
- `product_scale_crop`: row density, spacing, and ground-to-pattern hierarchy.
- `overall_product`: product thickness, binding, and approximate texture scale only.

Keep one integral woven system. For `jacquard-01`, use a low-profile coherent weave with staggered rows of softly twisted, slightly fuzzy elongated yarn bundles, fine pale binder threads, a clear horizontal grain, shallow relief, restrained soft lustre, and a narrow rounded serged edge. Fibre composition and manufacturing settings are unknown.

If an exact paired mapping example is later present, use it to estimate how boundaries soften, thin regions survive, and texture reads across scales. Never copy its historical motif or palette into the current design.

Use `task_reference_grounded` for usable task-specific real photos, `library_grounded` for bundled real assets, and `profile_only` without real evidence.

Failure signatures: printed surface, loop-pile rows, crochet, chunky knit, uniform rope braids, square bumps, pixel blocks, brick cells, appliqué, piping, or colour copied from reference products.

## `loop-pile`

- Surface: dense, short continuous loops with low sheen and restrained directional variation.
- Boundary: loops continue coherently through colour changes without disrupting small motifs.
- Default status without photos: `profile_only`, `provisional`.
- Failure signatures: visible cut ends, long shag, deep carving, detached loop clusters.

## `cut-pile`

- Surface: compact upright cut fibres with a soft tactile bloom and restrained directional tonal variation.
- Boundary: fibre direction may soften an edge locally while preserving product-scale geometry.
- Default status without photos: `profile_only`, `provisional`.
- Failure signatures: loop rows, harsh fur, long shag, unrelated directional stripes.

## Edge default

Unless the user specifies another finish, use a narrow continuous colour-matched `serged_overlock` outside the artwork. Keep its corners tidy and thickness proportionate.
