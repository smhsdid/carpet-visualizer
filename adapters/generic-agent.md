# Generic agent adapter

Use this adapter in an agent environment that can read repository files but may not recognise Codex skill metadata.

1. Load `SKILL.md`, then load only the references it routes to for the current task.
2. Attach or make available the current design source and each selected reference asset. Preserve their declared roles and authority order.
3. Use the same unified generation path for every design: complete current design first, declared construction references next, fixed lower-left detail, lightweight check, then automatic overview.
4. Save the final prompts, effective parameters, source hash, ordered attachments and output paths in the run record before generation; append the check result after generation.
5. If the environment cannot create images, return an `external_execution_required` packet containing the two final prompts, run record, attachment order, and quality checklist.

Use repository-relative paths. Keep provider-specific controls, model names, command syntax, and installation instructions outside the core workflow.
