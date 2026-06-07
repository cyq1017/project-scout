# Search Adapters

`prior-art-scout` owns the discovery protocol, report contract, coverage
confidence, and recommendation vocabulary. Search adapters only provide source
access.

Use capability names first. Map them to whatever tools the current agent
runtime provides.

## Capability Map

| Capability | Use For | Possible Tools |
| --- | --- | --- |
| `repo_search` | Open-source projects, libraries, tools, plugins, MCP servers | GitHub REST API, `gh search repos`, web search |
| `skill_registry_search` | Codex, Claude, and agent skills | `npx skills find`, registry website, GitHub search |
| `web_search` | Public products, docs, posts, comparison pages | native WebSearch, Exa, search MCP, browser search |
| `url_read` | Known URLs and primary-source pages | WebFetch, Jina Reader, curl, browser text extraction |
| `browser_inspect` | Dynamic pages, rendered content, interactive pages | Codex Browser, Chrome/Edge CDP, Playwright |
| `local_scan` | Local repos, local skills, ADRs, runbooks | `rg`, filesystem reads |
| `paper_search` | Research papers and academic prior art | arXiv, Semantic Scholar, publisher pages, web search |
| `community_search` | Pain points, alternatives, adoption signals | Reddit, V2EX, HN, Xiaohongshu, Twitter/X, forums |
| `job_market_search` | Hiring demand and workflow signals | job boards, LinkedIn-like sources, company career pages |

## Escalation Rules

Start with the lowest-permission route that can answer the question.

1. Use search or registry tools for candidate discovery.
2. Use URL readers for known primary sources.
3. Use browser inspection only when static reading fails or the page requires
   rendering or interaction.
4. Use logged-in browser state only when the user explicitly requests it and
   the target cannot be evaluated from public sources.
5. Do not automate social platforms by default. If used, mark account/platform
   risk and record the source as high-permission.

## Fallback Rules

| Failure | Fallback |
| --- | --- |
| GitHub API rate limited | Use manual candidates, `gh search repos`, or web search; record rate limit |
| Skills registry unavailable | Search GitHub/web for `skill`, `SKILL.md`, and registry names |
| Static URL reader fails | Try browser inspection or mark dynamic/login/blocked |
| Browser/CDP unavailable | Mark as unavailable and continue with lower-permission sources |
| Community platform blocked | Record blind spot instead of implying coverage |

## Search Log Requirements

For Formal Gate, record:

- source
- capability
- concrete tool when known
- query or URL
- result count
- used count
- status
- notes or errors

Quick Scan may summarize this in chat, but should still state uncertainty.

## Safety

- Do not store tokens, cookies, browser session data, or raw private page dumps.
- Do not perform account actions such as posting, liking, messaging, buying, or
  changing settings.
- Do not treat access through a user's logged-in browser as public evidence.
- Save raw search dumps only when the user explicitly asks for auditable
  artifacts.
