# Cross-Agent Skill Compatibility

## Problem

Skills should work across Codex, Claude, Hermes-like agents, and local agent
runtimes without depending on one product's private tool names.

## Pattern

Write skill instructions around capabilities first, concrete tools second.

| Capability | Possible Implementations |
| --- | --- |
| `repo_search` | GitHub REST API, `gh search repos`, web search |
| `skill_registry_search` | `npx skills find`, registry website, GitHub search |
| `web_search` | native WebSearch, Exa, search MCP, browser search |
| `url_read` | WebFetch, Jina Reader, curl, browser text extraction |
| `browser_inspect` | Codex Browser, Chrome/Edge CDP, Playwright |
| `local_scan` | `rg`, filesystem reads, local skill directories |

In `SKILL.md`, say what capability is needed and when to use it. In
agent-specific metadata or adapters, map that capability to available tools.

## Boundaries

- Do not require login, cookies, tokens, or user browser state by default.
- Do not require one package manager or registry as the only install path.
- Do not assume every agent can spawn subagents, use MCP, or run browser CDP.
- Keep deterministic CLI/library logic usable without skill support.

## Transfer

For every new skill, ask:

- What can run as plain instructions?
- What should be a deterministic script?
- What depends on optional tools?
- What must degrade to a recorded blind spot?

## Source

Derived from making `prior-art-scout` both a Python CLI/library and a skill
source repository.

## Last Verified

2026-05-27
