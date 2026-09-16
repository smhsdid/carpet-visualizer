# Material profiles

These profiles control visual construction only. Task-specific real material photos override a bundled material entry; a bundled entry overrides generic traits. Colours come from an explicit mapped colour card or, by default, the current design source.

## Construction-reference roles

| Role | Useful image | Authority |
| --- | --- | --- |
| `macro_detail` | Close, sharp view of yarns, loops, cut ends, or weave | Yarn geometry, interlacing, local relief |
| `product_scale_crop` | Larger surface area at a normal close-product distance | Texture density, spacing, hierarchy |
| `overall_product` | Whole product plus one visible edge or corner | Approximate thickness, binding, whole-product scale |

Use neutral or soft directional light, visible focus, and minimal perspective distortion. Strong filters, coloured lighting, extreme blur, or multiple constructions in one crop weaken evidence. A single useful photo is allowed; disclose its limited authority instead of inventing missing facts.

Normalise every directional observation into upright finished-product coordinates before writing the construction lock. A reference photographed sideways, folded, mirrored or rotated may still control yarn geometry and density, but its raw image axes do not control grain direction. Use declared edge and orientation evidence to state the product-relative coarse raised-yarn, fine cross-yarn and fine ground-anchor axes.

## `printed-low-pile`

- Surface: level, closely packed, low matte pile with colour carried in the fibres.
- Boundary: graphic regions remain clear with slight fibre softness and no structural relief.
- Default status without photos: `profile_only`, `provisional`.
- Failure signatures: woven grid, raised motifs, deep pile, embossed channels.

## `flatwoven`

- Surface: low-profile, matte warp-and-weft interlacing with restrained yarn irregularity and very low relief.
- Boundary: colour regions read as part of one woven plane; fine design lines remain fixed in the structure map.
- Scale: individual yarns are visible in the detail but compress into a coherent textile at overview distance.
- Default status without photos: `profile_only`, `provisional`.
- Failure signatures: plush pile, fur, oversized threads, basket-like blocks, printed smoothness.

## `wilton-flatweave`

When only a design is uploaded, use bundled `wilton-flatweave-01` and follow [the Wilton flatweave branch](wilton-flatweave-branch.md).

This is a library-calibrated Wilton flatweave visual profile. The supplied physical samples show a thin, low-relief surface formed from substantial multi-filament bundles in product-directional lanes. Open shadowed channels between lanes expose the finer interlacing; neighbouring lanes stagger their bundle ends, with visibly short and longer tapered units rather than one repeated length. The rounded bundle crowns rise only slightly above those fine threads, giving shallow shadows and restrained filament highlights without plush pile.

The design is yarn-built rather than applied. Pattern, ground, and boundary share one bundle size, row cadence, fine-thread system, relief, and finish. A boundary changes colour at bundle scale within the same surface; it does not turn into a smooth painted edge, motif-following cord, or separate raised layer.

Surface-build invariant: the source artwork is a hidden colour-region map while the visible image is reconstructed from the shared yarn system. A flat source-colour plate with a luminance, normal, emboss, displacement, noise, or generic texture layer is an overlay and must be rejected.

At macro scale, individual short bundles and the fine threads between them remain legible. At product scale, the construction compresses only through the declared camera transform while the supplied pattern remains fixed. Fibre, density, loom, and manufacturing process remain unspecified.

The manifest declares a generic real detail-camera anchor, optional quality anchor, and real construction reference. For a raking detail, attach the complete design first, camera anchor second, and real construction reference third; the design remains the sole pattern and colour authority. If a paired design matches the current source, its corresponding real photos remain forbidden generation references. The quality anchor teaches only exposure and general product-photo finish and must not influence yarn geometry. Do not attach conflicting patterned samples to one generation request.

Failure signatures: smooth printed colour, a source-RGB texture overlay, deep cut pile, tall open loops, inflated relief, applied motif layer, embroidery, piping, motif-following cord, chunky knit, crochet, braid, basket blocks, fur, shag, uniform oval-bead grids, closed equal-pitch lattices, equal-length aligned rows, or geometry copied from a reference product.

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
