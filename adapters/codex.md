# Codex adapter

Use this adapter when Carpet Visualizer is installed as a Codex skill.

- Invoke explicitly with `$carpet-visualizer`, or allow the normal skill-selection flow to choose it for carpet artwork rendering.
- Keep `SKILL.md` at the repository root. This is the portable workflow entrypoint and the GitHub installation target.
- `agents/openai.yaml` supplies Codex display metadata and a default prompt; it must not contain material rules that are absent from the core skill.
- Use the image-generation or image-editing capability available in the current Codex runtime. Record the actual backend, final prompts, effective parameters, attachment order, and output paths in the run record.
- Always use the unified strict pattern-preservation target and fixed lower-left detail. Generate the detail first, run the lightweight check, and then generate the overview automatically. Do not wait for user confirmation.
- If image generation is unavailable, return `external_execution_required` with the complete prompt packet and run record. A missing proof helper does not by itself block the visual route.

The workflow rules remain in `SKILL.md` so the same repository can be used elsewhere.
