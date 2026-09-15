# Local ComfyUI backend

Use this backend when a local GPU is available and the user wants replayable rendering rather than a semantic preview. The repository contains only the workflow contract and bootstrap scripts; Python environments, ComfyUI, caches, checkpoints, inputs, and outputs remain outside Git.

## Windows quick start

The default runtime is on `D:\AI\carpet-visualizer-runtime` so installations and transient downloads do not consume the system drive. Override `-RuntimeRoot` when another data drive is preferred.

```powershell
powershell -ExecutionPolicy Bypass -File scripts\install-local-backend.ps1
powershell -ExecutionPolicy Bypass -File scripts\run-local-render.ps1 "D:\path\to\artwork.jpg"
powershell -ExecutionPolicy Bypass -File scripts\run-hybrid-postprocess.ps1 "D:\path\to\accepted-semantic-master.png"
```

Run `scripts/doctor.py` with the runtime Python to capture the detected device, CUDA runtime, GPU compute probe, pinned ComfyUI commit, and model presence. A package listing alone is not sufficient evidence that GPU execution works.

## Portability contract

- Keep the runtime root configurable; never embed the developer machine path in prompts or generated workflow metadata.
- Read `config/runtime-lock.json` for the ComfyUI commit, PyTorch build and checkpoint identity.
- Recreate the pinned IP-Adapter Plus node and all model files through the installer; do not copy a developer virtual environment.
- The CUDA 13.0 profile is the supported NVIDIA/Windows baseline. Other vendors require a hardware-specific PyTorch install but use the same ComfyUI API and client workflow where their nodes are compatible.
- Do not copy a virtual environment between machines. Recreate it with the installer and keep models outside the skill checkout.
- Treat the baseline SDXL workflow as an integration proof. Add structure conditioning, material conditioning, tiled refinement and masked repair as versioned workflows; never silently change the baseline parameters.

## Baseline workflow

The client resizes the long edge to at most 1024 pixels on a 64-pixel grid, then runs low-denoise SDXL img2img with a fixed seed. It preserves the supplied artwork as the latent source and produces a complete overhead rug preview. This proves the PyTorch → CUDA → ComfyUI → checkpoint → API → output path; it does not by itself meet the final jacquard quality gate.

Use the default `-Denoise 0.28` only for topology-first integration checks. When the output merely reconstructs the artwork, make one controlled trial around `-Denoise 0.5` to `0.6` with 24–32 steps and inspect topology before accepting it. Higher denoise makes physical texture more visible but increases motif drift. Record the selected seed, steps, and denoise value with the output.

## Hybrid workflow

Use this as the production-oriented overview path when semantic image editing and the local GPU are both available:

1. Create a semantic master from the current artwork and bundled real construction references. The artwork owns topology and colours; the real photographs own weave, scale, edge construction and light response.
2. Reject structural drift before spending local compute.
3. Run `run-hybrid-postprocess.ps1`. It extracts grayscale high-frequency relief from the real product-scale and macro photographs, applies it without importing their colours or motifs, and submits the result to the pinned RealESRGAN model through ComfyUI.
4. Inspect the final 100% centre and boundary crops. Super-resolution is not proof of physical correctness; reject synthetic bead noise, halos, visible mirrored tiles or background texture.

The current IP-Adapter assets are installed and pinned for the next local repair stage. Do not claim IP-Adapter was used unless the submitted workflow record contains its nodes and weights.

Store generated results under the repository `output/` directory, which is ignored by Git. Keep user test artwork uncommitted unless the user explicitly asks to package it.
