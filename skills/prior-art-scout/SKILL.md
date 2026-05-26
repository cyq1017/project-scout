---
name: prior-art-scout
description: Discover existing solutions before building, buying, adopting, forking, extending, or writing new projects, skills, plugins, tools, MCP servers, products, papers, or internal assets. Use when the user asks whether something already exists; wants similar projects, alternatives, competitive research, prior-art research, build-vs-adopt guidance, deep research, a full comparison, or a report before roadmap, implementation, skill/plugin creation, or tool adoption decisions.
---

# Prior Art Scout

## Purpose

Use this skill as a pre-build and pre-adopt discovery gate. It is a search-enhanced brainstorm that turns "does this already exist?" into an evidence-backed reuse decision.

Core loop:

```text
define success criteria -> find candidates -> inspect sources -> compare overlap -> decide with confidence
```

Do not make irreversible decisions for the user. Provide evidence, options, confidence, and known blind spots.

## Mode Selection

Use **Quick Scan** when the user asks for a fast look, such as "is there anything like this", "有类似的吗", "find similar skills", "quickly check existing tools", or "does this already exist".

Use **Formal Gate** when the user asks for deep research, systematic research, a full comparison, a report, prior-art map, build-vs-adopt guidance, roadmap evaluation, or whether the direction is worth doing.

If the request is ambiguous, infer Quick Scan unless the user mentions report, deep research, formal evaluation, roadmap, ADR, backlog, or decision gate.

## Quick Scan Workflow

1. Identify the target type: `project`, `skill`, `plugin`, `tool`, `mcp_server`, `product`, `paper`, or `internal_asset`.
2. Define what "enough to answer" means for this scan.
3. Search the highest-value sources for the target type.
4. Include user-provided known candidates first.
5. Return a concise table of candidates and a short recommendation.
6. State uncertainty briefly.

Do not write files by default in Quick Scan.

## Formal Gate Workflow

1. Create a Discovery Brief. See `references/discovery-brief.md`.
2. Include known candidates first, then search for additional candidates.
3. Route sources by target type. See `references/source-routing.md`.
4. Apply coverage protocol. See `references/coverage-protocol.md`.
5. Normalize candidates into comparable metadata.
6. Run `project-scout` CLI/library when available for deterministic scoring and report generation.
7. Add recommendation, confidence, risks, unknowns, search summary, and blind spots.
8. Write Markdown and JSON outputs. See `references/report-contract.md`.
9. Summarize the result in chat with links to generated files.

Do not push, publish, create issues or PRs, or modify ADR/backlog files unless the user explicitly requests that action.

## Recommendation Set

Use `Adopt`, `Borrow`, `Integrate`, `Fork`, `Extend`, `Write New`, `Avoid`, `Ignore`, or `Monitor`. See `references/recommendation-rubric.md`.

Always separate:

- decision recommendation
- decision confidence
- coverage confidence

## Evidence Rules

- Prefer primary sources: official repo, docs, package pages, skill registry entries, project websites, papers, and user-provided files.
- Mark unverified metadata clearly.
- Do not treat stars, popularity, or SEO ranking as adoption proof.
- Record source, query, result count, and errors in the search log for Formal Gate.
- Save raw search dumps only when the user explicitly asks for an auditable raw record.
- Follow safety limits in `references/safety.md`.

## Using `project-scout`

If this repository is available locally, prefer:

```bash
project-scout report \
  --brief path/to/brief.json \
  --candidates path/to/candidates.json \
  --out-json path/to/report.json \
  --out-md path/to/prior-art-map.md
```

For live GitHub search:

```bash
project-scout report \
  --brief path/to/brief.json \
  --github-query "query terms" \
  --github-limit 10
```

If unauthenticated GitHub API is rate-limited, fall back to manual candidates or search results from other sources and record the rate limit in the search log.

## Skill Orchestration

Use adjacent skills as adapters, not replacements:

- Use search/web skills for source discovery when live web access is needed.
- Use skill-creator only when the outcome is creating or changing a skill.
- Use code-reviewer after changing code.
- Use verification-before-completion before claiming checks pass.

This skill owns the discovery protocol and report contract. Other skills provide source access, implementation help, review, or packaging.

## Output Style

For Quick Scan, lead with the practical answer and include a compact candidate table.

For Formal Gate, lead with generated artifact links, then summarize:

- top recommendation
- confidence
- top 3-5 candidates
- major borrow/adopt/integrate signals
- major avoid or unknown signals
- next decision step
