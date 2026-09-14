# Generic agent adapter

Use this adapter in an agent environment that can read repository files but may not recognise Codex skill metadata.

1. Load `SKILL.md`, then load only the references it routes to for the current task.
2. Attach or make available the current design source and each selected reference asset. Preserve their declared roles and authority order.
3. Match the available image backend against [rendering capabilities](../CAPABILITIES.md). Use image editing when possible; otherwise create from attached references and the final prompts.
4. If the environment cannot create images, return an `external_execution_required` packet containing the two final prompts, render lock, attachment order, and quality gate.

Use repository-relative paths. Keep provider-specific controls, model names, command syntax, and installation instructions outside the core workflow.
