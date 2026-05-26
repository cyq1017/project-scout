# Prior Art Scout Skill Design

## Intent

`prior-art-scout` is a reusable discovery skill for checking existing solutions before starting work, adopting a tool, writing a skill/plugin, or changing a roadmap. It generalizes `project-scout` from "similar project discovery" into a pre-build and pre-adopt gate.

The skill answers: what already exists, what can be reused, what should be avoided, and whether the current evidence supports adopt, borrow, integrate, fork, extend, write new, ignore, or monitor.

## Modes

Quick Scan is a search-enhanced brainstorm. It runs when the user asks natural questions like "is there anything like this", "有类似的吗", "quickly check existing tools", or "find similar skills". It should usually avoid clarification unless the target is ambiguous. It returns a compact candidate table, a short recommendation, and uncertainty notes. It does not write files by default.

Formal Gate runs when the user asks for deep research, systematic research, a full comparison, a report, build-vs-adopt guidance, roadmap evaluation, prior-art map, or a decision before implementation. It asks for missing critical context, writes Markdown and JSON reports, records a structured search log, and includes recommendation confidence.

## Scope

Initial target types:

- `project`
- `skill`
- `plugin`
- `tool`
- `mcp_server`
- `product`
- `paper`
- `internal_asset`

MVP sources are GitHub search, manual URLs, skills registry search, and user-provided local/internal paths. Web, Product Hunt, Hacker News, Reddit, package registries, paper search, and MCP registries can be added later as adapters.

## Data Model

Formal Gate uses a `DiscoveryBrief` with:

- `name`
- `target_type`
- `intent`
- `goal`
- `keywords`
- `users_or_consumers`
- `ecosystems`
- `must_have`
- `nice_to_have`
- `exclusions`
- `known_candidates`

The current `project-scout` core can remain compatible by mapping the discovery brief into the existing project brief fields. This avoids breaking the MVP while letting the skill layer support broader use cases.

## Recommendation Model

Use one shared recommendation set:

- `Adopt`
- `Borrow`
- `Integrate`
- `Fork`
- `Extend`
- `Write New`
- `Avoid`
- `Ignore`
- `Monitor`

Formal Gate must separate recommendation from confidence. Confidence should be `Low`, `Medium`, or `High`, with explicit reasons such as candidate count, source quality, missing license metadata, stale update metadata, rate limits, or reliance on manual candidates.

## Reports

Formal Gate writes:

- Markdown report for humans
- JSON report for machines

Markdown should include Executive Summary, Search Summary, Coverage Matrix, Similar Candidates, Overlap Matrix, What To Adopt / Integrate / Borrow, What To Avoid, Recommendation And Confidence, Coverage Confidence And Blind Spots, Useful Positioning, Risks And Unknowns, and Suggested ADR / Backlog / Skill Updates.

JSON should include the brief, generated timestamp, mode, summary, decision, coverage, structured search log, candidates, overlap matrix, recommendations, risks, and suggested updates. Raw search dumps are not saved by default; save them only when the user asks for a complete audit trail.

## Coverage Protocol

The skill should not claim exhaustive search. It should claim defensible coverage. Formal Gate must define required source classes, record searched/skipped/rate-limited sources, expand queries beyond the user's wording, perform snowball and negative searches when useful, and state stop criteria.

Coverage confidence is separate from decision confidence. A strong recommendation can still have Medium coverage confidence if web/community/product sources were skipped or rate-limited. Reports must include known blind spots.

## Skill Orchestration

The repository should use other skills as adapters rather than absorb their responsibilities:

- Web Access or agent-reach for live web and browser source access.
- find-skills for ecosystem discovery before creating new skills.
- skill-creator for scaffolding and validating new skill folders.
- code-reviewer and verification-before-completion for code changes.

`prior-art-scout` owns the discovery protocol, candidate normalization contract, coverage protocol, and recommendation rubric.

## Safety

The skill does not push, publish, create issues or PRs, or modify ADR/backlog files unless the user explicitly requests that action. It should not store tokens or credentials. It should prefer local-first deterministic scoring and primary sources. It should mark unverified metadata clearly.

## Packaging

Maintain the skill source in this repository under `skills/prior-art-scout`. For local use, install or copy it to the user-level Codex skills directory. For community distribution, publish the repository with the skill source, CLI/library, examples, and report schema. Public release and promotion require an explicit user request before pushing or publishing.

The public repository should present the skill as:

```text
Before you build it, scout it.
```

The first examples should cover project discovery, skill discovery, and plugin/tool adoption so users understand this is broader than GitHub repo search.
