# Cross-Agent Protocol

Use this reference to keep `prior-art-scout` behavior stable across Codex,
Claude, GPT-style agents, and local agent runtimes.

## Capability First

Write and execute plans in capability terms first, then map to available tools:

| Capability | Examples |
| --- | --- |
| `repo_search` | GitHub REST API, `gh search repos`, web search |
| `skill_registry_search` | `npx skills find`, registry website, GitHub search |
| `web_search` | native web search, search MCP, browser search |
| `url_read` | WebFetch, Jina Reader, curl, browser extraction |
| `browser_inspect` | Codex Browser, Chrome CDP, Playwright |
| `local_scan` | `rg`, filesystem reads |
| `report_engine` | `.venv/bin/project-scout report`, `python -m project_scout.cli report` |

## Execution Rules

- Use the lowest-permission capability that can answer the question.
- If a capability is unavailable, record it as a source gap or blind spot.
- Prepare structured candidates before running the report engine.
- Run `project-scout` for deterministic scoring, coverage, dashboard, and
  Markdown/JSON output whenever the engine is available.
- Do not hand-write engine-owned fields unless the engine is unavailable; if you
  must do so, mark the result provisional.
- Do not require login, tokens, browser cookies, subagents, or MCP availability
  for the default path.

## Agent Handoff Checklist

Before finishing a Formal Gate, confirm:

- Discovery brief is explicit enough to search.
- Query matrix was applied or skipped with a reason.
- Known candidates were included or recorded missing.
- Source log records source, query, status, result count, and used count.
- Candidate JSON is structured enough for `project-scout`.
- Report engine was used, or the missing engine was called out.
- Discussion cites report evidence and blind spots.

## Forward-Test Prompt Shape

Use prompts like this when testing another agent:

```text
Use prior-art-scout at <skill path> to run a Formal Gate for this target:
<brief>

Write draft outputs under /tmp. Use available public sources. If a source or
engine is unavailable, record the gap rather than inventing coverage.
```

Do not include the expected answer in the test prompt. The goal is to observe
whether the skill transfers across agents.
