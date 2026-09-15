# 画稿到地毯实物图：应用与技术研究

研究日期：2026-09-14  
适用范围：当前 `carpet-visualizer` skill 的开发阶段；目标是做设计评审和肌理筛选，不替代打样或生产确认。

## 结论先行

现有 skill 的方向是正确的：把当前设计、物理肌理、拍摄风格、历史配对样本分开，并先做肌理细节再做产品全景。下一阶段的主要收益不在于把提示词写得更长，而在于：

1. 把设计稿转成“图案/颜色/轮廓的硬约束”，把肌理参考转成“表面结构的软约束”。
2. 按后端区分工作流：内置生图适合语义约束和小步编辑；本地可控工作流适合 ControlNet、IP-Adapter 和遮罩修复；需要大量变体或接近生产的展示时再考虑 Blender/PBR。
3. 用“构造 + 尺度 + 光照反应 + 边界行为”描述肌理，而不是只写“高级、柔软、真实、细腻”。
4. 把每次失败记录成类别：图案漂移、颜色泄漏、肌理替换、跨尺度不一致、边缘错误。一次只修改一个类别。

## 一手资料与对当前项目的启示

### 1. 结构控制：ControlNet

[ControlNet 官方仓库](https://github.com/lllyasviel/ControlNet)的核心做法是给扩散模型增加独立的条件控制分支，示例覆盖 Canny、深度、法线、线稿、分割等条件。对地毯设计来说，最有用的不是“让模型自由理解这张图”，而是给它一张明确的结构条件：轮廓/线稿用于保边界，分割或颜色区域用于保区域关系，深度或法线只用于有明确起伏的产品场景。

建议的结构条件优先级：

- 纯平面、几何清晰的设计稿：区域分割/颜色遮罩 > 线稿或边缘。
- 只有黑白线稿：线稿或 Canny，但要接受细线可能断裂、合并的风险。
- 已有产品照片、需要换肌理或修局部：image-to-image + inpainting；不要靠一次全图重绘解决。

### 2. 参考图解耦：IP-Adapter

[IP-Adapter 官方仓库](https://github.com/tencent-ailab/IP-Adapter)把参考图作为图像提示单独注入，并明确提供 image-to-image、inpainting 以及与 ControlNet 组合的示例。它还提醒：默认图像处理会中心裁剪，非方形参考图可能丢失边缘信息；地毯通常是长方形，因此肌理参考应使用正方形留白版、同尺度裁剪版，或分别提供 macro/product-scale/overall 三个角色，不要把一张长图直接当成唯一参考。

[Diffusers 的 IP-Adapter 文档](https://huggingface.co/docs/diffusers/using-diffusers/ip_adapter)明确展示了“IP-Adapter 负责图像特征、ControlNet 负责结构条件”的组合。对当前 skill 的对应关系是：设计稿负责拓扑，肌理照片负责物理外观，不能把两者混成一个“风格参考”。

这也是为什么建议把当前 skill 的 authority block 继续保留，但不要把它当作唯一控制手段：提示词可以声明“这张图只负责什么”，真正的隔离要落到不同的输入分支和后验检查上。

### 3. image-to-image、inpainting 与参数含义

[Diffusers image-to-image 文档](https://huggingface.co/docs/diffusers/using-diffusers/img2img)说明，`strength` 越高，向初始图加入的噪声越多，结果越有创造性、也越容易偏离原图；接近 1 时基本会忽略初始图。[Inpainting 文档](https://huggingface.co/docs/diffusers/main/using-diffusers/inpaint)说明遮罩白色区域会被重绘，黑色区域保留。

这支持一个很实用的规则：

- 设计拓扑错误：重新以设计稿为 edit target，不要提高创造性。
- 肌理不够明显：只提高局部肌理细节或更换肌理参考，不要整张重绘。
- 包边错误：只遮罩边缘区域进行修复。
- 颜色漂移：换成中性肌理参考并重申颜色权威，不要用“更准确”这种模糊要求。

### 4. 可组合的本地工作流：ComfyUI

[ComfyUI 官方仓库](https://github.com/Comfy-Org/ComfyUI)提供节点式工作流、ControlNet、inpainting、工作流 JSON 和种子复现能力；[官方 IPAdapter 节点仓库](https://github.com/comfyorg/comfyui-ipadapter)还提供了多种 IP-Adapter 工作流示例。它适合作为以后需要反复比较肌理、控制参数、保存可复现实验时的后端。

但当前不建议一开始就训练模型或搭建很大的节点图。先把输入角色、肌理档案和质量标签稳定下来，再决定是否迁移到本地可控工作流。

### 5. 物理肌理词汇：不要只说“毛感”

[Carpet and Rug Institute 的构造说明](https://carpet-rug.org/carpet-for-business/finding-the-right-carpet/)指出，地毯的外观首先由 loop、cut 或两者组合的构造决定；密度、纱线捻度、绒高和背衬也会影响外观与性能。[其住宅地毯说明](https://carpet-rug.org/carpet-for-homes/selecting-the-right-carpet/)进一步区分了 cut pile、loop pile、multi-level loop 和 cut-loop 的表面效果。

因此，提示词应先回答“纱线如何形成表面”，再回答“看起来有多舒服”：

| 维度 | 应描述什么 | 示例词 |
| --- | --- | --- |
| 构造 | 织、印、簇绒、绒圈、割绒、混合构造 | `integral woven jacquard`, `flatwoven warp-and-weft`, `short level loop`, `compact cut pile` |
| 纱线 | 纱线是短圈、割断纤维、扁平纱束、隆起的环拱/浮长纱束还是细丝 | `elongated folded or loop-like bundles`, `short continuous loops`, `upright cut fibres` |
| 组织 | 纱线之间如何交错、排列和连续；方向必须先归一到直立成品坐标 | `coarse raised yarns vertical`, `fine cross yarns horizontal`, `fine recessed anchor yarns vertical` |
| 尺度 | 微观可见什么，产品距离要压缩成什么 | `macro-readable fibres`, `product-scale texture compresses into one continuous textile` |
| 起伏 | 整体产品厚度与局部表面高低要分开；记录平整、明显微观起伏、多高度或深雕刻 | `thin rug body with pronounced local relief`, `level surface`, `multi-level loop relief` |
| 光照反应 | 粗糙度、哑光、柔和高光、方向性 | `matte to soft low lustre`, `restrained directional tonal variation`, `no plastic gloss` |
| 表面细节 | 毛羽、轻微不规则、磨损或压痕 | `slight fibre fuzz`, `restrained yarn irregularity`; 只有有证据时才写 `worn`, `crushed`, `mottled` |
| 边缘 | 包边、厚度、角部处理 | `narrow rounded continuous serged edge`, `tidy corners` |
| 禁止替代 | 防止模型把肌理换成别的东西 | `not printed`, `not fur`, `not chunky knit`, `not crochet`, `not braided rope`, `not basket weave`, `not tile grid` |

## 对当前 `jacquard-01` 的具体建议

我检查了当前三张 neutral generation input。它们已经形成较好的三尺度证据链：

- macro：能看到带轻微毛羽的粗凸纱束、较细交织纱，以及沉在隆起纱束下方的细线状固定纱；照片中的表观方向必须换算为直立成品坐标，局部偏亮也只作为光照和凹凸造成的同色系变化，不作为固定纱色。
- product-scale crop：能看到更规则的行列、密度和纹理尺度；方向必须先换算到直立成品坐标，不能直接照搬照片轴向。
- overall：能看到整体厚度和连续包边；适合控制产品尺度和边缘，但背景、透视和杂物会削弱其作为肌理生成输入的纯度。

方向解释必须以直立设计稿和成品地毯为坐标。当前 product-scale 与 overall 的 neutral 生成输入已经把像素实际归一到直立成品方向，并清除了 EXIF 旋转依赖；生成时直接使用，不再二次旋转。粗凸主纱沿纵向排列，较细交织纱沿横向穿插，另有较细的纵向固定纱沉在隆起主纱下方。三套纱线的颜色都跟随设计稿所在颜色区域，不默认使用浅色或白色固结纱。

建议保留现有素材，同时在 manifest 中增加以下信息：

```yaml
prompt_axes:
  construction: "thin-bodied integral relief-rich jacquard weave, not printed"
  orientation: "upright finished-rug coordinates; coarse raised yarns vertical, fine cross yarns horizontal, fine recessed ground/anchor yarns vertical"
  yarn: "two related scales of short soft multi-filament folded floats, with larger dominant and smaller secondary tapered crowns, visible twist and fine fibre fuzz"
  organization: "vertical crowns occupy about 55–65% visible exposure; horizontal fine yarns remain continuously readable at about 25–35% through plain fields, motifs and boundaries; fine vertical ground yarns stay recessed"
  relief: "compact pronounced micro-relief physically created by over-under interlacing and compression while the overall rug body remains thin"
  finish: "soft satin lustre with fine strand highlights; no hard plastic gloss"
  overview_scale: "individual bundles reduce in apparent size but retain a tactile woven jacquard read at product distance"
  boundary: "one three-yarn jacquard system continues across colour changes; yarn exposure, coverage and relief distribution may vary while calibre, spacing and interlacing stay stable"
  yarn_colour: "all visible yarn systems inherit the local design-region colour; no fixed pale or white binder grid"
  edge: "narrow rounded continuous serged edge with tidy corners"
anti_substitutions:
  - printed smooth surface
  - chunky knit
  - crochet
  - freestanding braided rope or cord
  - long open loops or oversized tubular stitches
  - basket weave
  - square or pixel blocks
  - uniform tufted loop-pile carpet with independent upright loops
  - flat plain weave with no raised jacquard bundles
  - long fur or shag
```

这里必须区分两个尺度：整体地毯本体较薄，但局部纱束可以较粗并形成明显的环拱、浮长和凹凸。`overview_scale` 的目标不是把这些纱束压平，而是让它们在全貌距离缩小成连续、仍有触感的提花肌理。真正需要排除的是脱离细固结纱体系的独立粗绳、积木格或另加的簇绒层。整体参考图仍建议制作“只保留地毯本体、裁去大部分背景”的 derived crop；这属于输入清洁，不改变原图审计资产。

## 推荐的 v0.2 工作流

### A. 仍使用内置生图预览时

1. 上传设计稿，明确它是唯一的图案、轮廓和颜色来源。
2. 上传一张中性 macro 肌理图和一张产品尺度肌理图；如需包边，再提供整体边缘图。每张图写清楚角色。
3. 先生成一个跨越两种颜色区域的肌理细节，检查纱线是否连续、边界是否保持、肌理有没有变成印刷或毛皮。
4. 再用当前设计稿 + 通过检查的细节图生成 overview。不要重新加入会带来历史图案或颜色的产品照片。
5. 失败时只做一次针对性编辑：例如“只修复包边，保持图案、颜色、相机和肌理不变”。

[OpenAI Academy 的图像提示建议](https://openai.com/academy/image-generation/)强调，清晰具体比堆叠形容词更可靠；少量参考图通常比大量参考图更容易控制；编辑时要明确“改变什么、保持什么”，并用小步、单变量的修订维持一致性。这与当前 skill 的 render lock 和 targeted retry 设计是一致的。

### 6. 进一步值得关注的研究方向

- [ControlNet 论文](https://arxiv.org/abs/2302.05543)说明了额外空间条件控制的基本原理，适合作为“区域图 + 边缘图”双控制的理论依据。
- [SDEdit 论文](https://arxiv.org/abs/2108.01073)明确讨论了真实性和输入忠实度之间的权衡，支持“低强度 image-to-image + 局部 mask”的策略，而不是全图高强度重绘。
- [InstantStyle 官方仓库](https://github.com/instantX-research/InstantStyle)展示了只在特定 attention block 注入风格、降低参考图内容泄漏的思路，可作为未来 style-only 肌理分支的参考，但它本身不是拓扑约束。
- [Training-free Color-Style Disentanglement 论文](https://arxiv.org/abs/2409.02429)把颜色和风格拆成不同分支，对“彩色历史肌理图污染当前颜色”的问题有启发意义；它不是地毯专用方案，先作为实验项，不要直接当作生产保证。
- [ControlNet++ 论文](https://arxiv.org/abs/2404.07987)用“输出重新提取控制条件，再与输入条件比较”的一致性反馈提高控制效果。当前无需训练它，但可以先把“输出反提取后回比设计稿”加入质量诊断。

### B. 以后迁移到 ComfyUI / Diffusers 时

可以把工作流拆成四条输入：

```text
design artwork
  -> region mask / line or edge control -> topology preservation

neutral material references
  -> IP-Adapter or reference branch -> yarn / weave / finish

scene reference
  -> camera / light / background only

local defect mask
  -> inpainting -> edge, corner, or boundary repair
```

建议新增两张由设计稿派生的控制图：`region_map`（不同颜色区域的分割/标签图）和 `edge_map`（轮廓、主要边界或 soft-edge 图）。前者锁区域、邻接和负空间，后者锁轮廓和细线。肌理参考不得进入这两条结构分支。

不要把 Canny、IP-Adapter、肌理照片、历史实物图和风格图的权重一次调高。先固定设计结构，再逐个增加肌理证据；每轮只比较一个变量，并保存输入、提示词、参数、seed、输出和失败标签。至少独立记录 `pattern_control_scale`、`material_ip_scale`、`denoise_strength`、mask blur/dilate、`control_guidance_start/end` 和 aspect padding，不要用一个笼统的 `reference_strength` 代替所有参数。

生成顺序取决于目标：如果目标是快速筛选“这张肌理参考是否适合”，`detail_first` 很合理；如果目标是严格的跨尺度一致性，建议先生成通过结构检查的 overview，再从同一结果裁剪并局部 inpaint 出 material detail。这样 detail 和 overview 共享同一产品、颜色和纹理层级，代价是前期需要先解决全景中的结构问题。

在输出端增加轻量回比：重新提取 region/edge 条件，检查 motif 数量、区域 IoU、边界 F-score、邻接关系；颜色区域可在对应 mask 内比较 LAB 或 ΔE。它们是诊断信号，不应被包装成制造精度。

### C. 什么时候考虑 Blender

如果目标变成“同一地毯要生成几十个稳定角度/颜色/场景”，或需要准确控制透视、厚度、包边和光照，建议把地毯作为平面/薄体模型，使用 UV 设计图和肌理贴图，再用程序化织物纹理或真实扫描肌理渲染。Blender 的 [Principled BSDF 文档](https://docs.blender.org/manual/en/5.2/render/shader_nodes/shader/principled.html)说明了 sheen 可模拟表面微小纤维的柔和边缘反射；[Normal Map 文档](https://docs.blender.org/manual/en/4.3/render/shader_nodes/vector/normal_map.html)说明法线图应与 UV 对齐并作为 Non-Color 数据处理。这里的 Blender 是未来的稳定渲染后端，不应在当前预览型后端中假称已经使用。

## 建议补充到 skill 的最小字段

不必立刻重写全部文档，建议先补四项：

```yaml
backend_strategy:
  preview_only:
    reference_budget: 3
    preferred_sequence: [material_detail, product_overview, targeted_retry]
  controllable_local:
    structure_condition: [region_map, edge_map]
    material_condition: ip_adapter_or_reference_branch
    repair: masked_inpainting
    independent_controls:
      - pattern_control_scale
      - material_ip_scale
      - denoise_strength
      - mask_blur_or_dilate
      - control_guidance_start_end
      - aspect_padding

material_prompt_axes:
  construction: "..."
  yarn_geometry: "..."
  organization: "..."
  scale_behavior: "..."
  relief: "..."
  finish: "..."
  boundary_behavior: "..."
  edge_geometry: "..."

evaluation_record:
  topology: pass|caveat|fail
  material: pass|caveat|fail
  cross_scale_consistency: pass|caveat|fail
  colour_authority: pass|caveat|fail
  edge_finish: pass|caveat|fail
  region_iou: optional
  boundary_f_score: optional
  colour_delta_e: optional
  failure_tags: []
```

## 可直接试用的 jacquard 英文提示词

### Material detail

```text
Use the current design artwork as the only authority for the existing outline, motif topology, region boundaries and colours. Use the stored construction generation inputs directly in their upright finished-rug orientation. Show the complete lower-left corner as an ultra-close grazing-diagonal macro commercial-product photograph. Place the lens nearly level with the near binding, roughly 8–12 degrees above the rug plane, and look diagonally across the surface. Make the near binding side face prominent, with strong surface recession, near-to-far yarn-scale compression and gentle distant focus falloff. Let rug surface fill about 96–98% of the frame; retain the complete near corner junction, short segments of both bindings and only enough adjacent motif to locate it. Render one thin-bodied three-yarn jacquard. Coarse raised crowns run vertically and occupy about 55–65% visual exposure. Naturally interleave larger dominant crowns with smaller secondary crowns about 1.3–1.6 times narrower. Keep finer horizontal cross yarns continuously readable at about 25–35% through plain fields, motifs and colour boundaries. Fine vertical ground or anchoring threads remain recessed. Each soft multi-filament float bends over horizontal yarns, compresses at ties and returns into the ground. Every yarn follows its local design colour. Use bright high-key grazing light, clean exposure, crisp medium-high contrast and luminous strand highlights while keeping near and central interlacing sharp.
```

### Product overview

```text
Use the current design artwork as the exact pattern and colour source. Use the stored construction generation inputs directly in their upright finished-rug orientation: coarse raised yarns run vertically, finer cross yarns run horizontally, and fine recessed ground or anchoring yarns also run vertically beneath the raised crowns. Show the complete rug as a bright crisp commercial catalogue photograph on a warm-white or light neutral surface, using a standing-observer downward camera with a restrained near-overhead angle and mild natural near-to-far perspective. Keep the near lower edge only slightly larger than the far upper edge; keep the rug upright and square to the frame, match the canvas to its aspect ratio where possible, and fill about 92–96% of the frame while retaining the entire bound outline and all four corners. Use high-key directional studio daylight, clean exposure, clear colours, luminous whites, crisp medium-high contrast and a narrow defined contact shadow. Render the same thin-bodied integral relief-rich jacquard weave: short soft multi-filament folded floats form tapered, slightly irregular raised crowns with visible twist and fine fibre fuzz. Their long axes and end-to-end chain rhythm run vertically. Each coarse float bends over finer horizontal cross yarns, compresses at ties and sinks back between crowns; fine vertical ground or anchoring threads remain recessed beneath them. Every yarn system follows the colour of its local design region. Maintain compact relief created by over-under interlacing and yarn compression, warm clean satin highlights and a narrow rounded continuous serged edge. At this distance the units reduce in apparent size but retain a fine tactile jacquard grain. Pattern and ground may vary in yarn exposure, coverage and relief distribution while coarse-yarn calibre, fine-yarn spacing and three-system interlacing remain stable. Preserve the outline, motif count, region adjacency, symmetry and negative space; no grey veil, muddy desaturation, underexposure, flat subdued grading, printed smoothness, fur, loose chunky knit, crochet, long open loops, oversized tubular stitches, freestanding braided rope, basket weave, square blocks, applied embroidery, repeated identical capsule bumps, extra objects, labels or watermark.
```

## 当前阶段的优先级

1. 先补 `prompt_axes`、`anti_substitutions` 和整体边缘的干净 crop。
2. 用同一张测试设计跑 6–10 次小实验，每次只改变一项：肌理描述、参考图数量、细节锚点或边缘修复。
3. 把结果按质量 rubric 打标签，并把失败图保留为回归测试证据。
4. 只有当“设计拓扑保持”和“肌理跨尺度一致”在内置预览中已经稳定，再评估 ComfyUI/Diffusers；只有需要稳定多角度或大量变体时再评估 Blender。

视觉样图仅供评审使用——颜色、纱线、绒高、密度和构造仍需通过实物打样确认。
