# GitHub Source Pattern

## Use When

Use GitHub for open-source projects, libraries, tools, MCP servers, plugins,
skills with source repos, and code-backed products.

## Routes

| Need | Preferred Route |
| --- | --- |
| Deterministic repo search | GitHub REST API or `project-scout --github-query --github-timeout <seconds>` |
| Manual exploration | `gh search repos "<query>" --sort stars --limit N` |
| Code-specific discovery | GitHub code search when available |
| Metadata verification | repo README, license, topics, releases, issues, commits |

## Metadata To Capture

- name and URL
- description and topics
- stars
- last update
- primary language
- license
- README summary
- obvious integrations or related projects

## Pitfalls

- Stars are weak adoption evidence.
- Last update alone does not prove maintenance quality.
- README claims need to be checked against code, releases, or docs when the
  decision depends on them.
- API rate limits should be recorded, not hidden.
- Use `--no-github-readme` when source collection should avoid the extra
  best-effort README request per result.
- Zero-result searches should be recorded as `empty`; network, DNS, timeout, or
  rate-limit failures should be recorded as `failed` or `rate_limited`, not
  silently treated as coverage.

## Last Verified

2026-06-20
