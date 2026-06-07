# project-scout Agent Notes

## Scope

This is an independent CLI/library project. It is not part of Conductor Core. Future integrations may wrap it as a Codex/Claude skill or call it from Conductor as a plugin/gate.

## Safety

- Do not push, publish, release, or open pull requests unless the user explicitly asks in the current task.
- Do not store GitHub tokens or other credentials.
- Keep all default workflows local-first.
- Prefer deterministic parsing and scoring. LLM summarization must remain optional.
- Do not add broad crawler behavior to the MVP.

## Development

- Use Python.
- Keep the CLI thin and route behavior through `project_scout` library modules.
- Write fixture-based tests for network-shaped inputs.
- Avoid tests that depend on live GitHub availability.
- Run `pytest` before claiming the project is working.

## Report Contract

Default outputs:

- `project-scout-report.json`
- `docs/research/YYYY-MM-prior-art-map.md`

Do not commit ad hoc generated reports at the repo root. Use `/tmp` for smoke
and local validation outputs, or place curated examples under `examples/` and
`docs/research/`.

Required Markdown sections are documented in `docs/report-schema.md`.
