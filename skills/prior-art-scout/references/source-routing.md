# Source Routing

Choose sources based on target type and mode.

## MVP Sources

- GitHub search: projects, tools, libraries, MCP servers, plugins.
- Skills registry: Codex, Claude, and agent skills.
- Manual URLs: user-provided candidates, product pages, papers, repos, docs.
- Local/internal paths: user-provided local repositories, runbooks, ADRs, skills, or plugin directories.

Use web access or browser automation skills only as source adapters. `prior-art-scout` owns the discovery protocol, coverage judgment, and report contract.

## Target Defaults

| Target type | Primary sources | Notes |
| --- | --- | --- |
| `project` | GitHub, manual URLs | Prefer repo metadata, README, license, activity. |
| `skill` | skills registry, GitHub, local skills | Compare trigger scope, workflow, resources, install path. |
| `plugin` / `tool` | GitHub, package docs, manual URLs | Compare integration boundary, API, runtime, maintenance. |
| `mcp_server` | GitHub, MCP registries when available, manual URLs | Compare transport, tools exposed, auth, security model. |
| `product` | official site, docs, community references | Do not infer claims from SEO pages alone. |
| `paper` | paper databases, publisher pages, arXiv, manual URLs | Prefer abstract, method, citations, code links. |
| `internal_asset` | user-provided paths only | Do not read private assets unless the user asks. |

## Query Patterns

Start with combinations of:

- target name and synonyms
- core outcome
- ecosystem or runtime
- "alternative", "open source", "plugin", "skill", "MCP", "agent", "desktop", "CLI", or other shape words
- exclusions as negative filters when supported

For Formal Gate, record every query in the structured search log.

## Adjacent Skill Use

- Use `find-skills` or skills registry commands for skill ecosystem discovery.
- Use browser/web-access skills for dynamic pages, login-required pages, or community pages.
- Use `skill-creator` only after the user decides to create or update a skill.
- Use review and verification skills after implementation changes, not during source discovery.
