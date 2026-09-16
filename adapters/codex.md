# Codex adapter

Use this adapter when Carpet Visualizer is installed as a Codex skill.

- Invoke explicitly with `$carpet-visualizer`, or allow the normal skill-selection flow to choose it for carpet artwork rendering.
- Keep `SKILL.md` at the repository root. This is the portable workflow entrypoint and the GitHub installation target.
- `agents/openai.yaml` supplies Codex display metadata and a default prompt; it must not contain material rules that are absent from the core skill.
- Use the image-generation or image-editing capability available in the current Codex runtime. Record the actual backend in the render lock rather than assuming a backend name.
- If the runtime is preview-only, it cannot pass `topology_mode: exact` without an aligned structure proof. Use it only for an explicitly requested approximate concept; otherwise return `external_execution_required`.

The Codex GitHub installation instructions belong in the repository README. The workflow rules remain in `SKILL.md` so the same repository can be used elsewhere.
