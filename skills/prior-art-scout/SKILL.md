---
name: prior-art-scout
description: Run pre-build and pre-adopt technical due diligence for build-vs-adopt decisions. Use when the user asks whether something already exists, wants similar projects or alternatives, needs competitive or prior-art research, asks whether to build, buy, adopt, integrate, fork, extend, borrow from, or write new, or needs a report before roadmap, implementation, skill/plugin creation, tool adoption, MCP server work, product positioning, or technical direction decisions.
---

# Prior Art Scout

## Overview

Use this skill as a technical due-diligence gate before building or adopting a
project, skill, plugin, tool, MCP server, product, paper, or internal asset.

The job is to produce defensible evidence, not to prove the market is empty or
make irreversible decisions for the user.

## Core Process

1. Classify the mode: Quick Scan or Formal Gate.
2. Capture the target, must-have requirements, exclusions, and known candidates.
3. Plan coverage by target type before searching.
4. Collect candidates from bounded sources and record queries, errors, and gaps.
5. Normalize candidates into comparable metadata and evidence categories.
6. Use the `project-scout` CLI/library for deterministic scoring and report generation when available.
7. Interpret the report into build-vs-adopt guidance, positioning, and next checks.
8. Verify artifacts, confidence, blind spots, and exit criteria before claiming completion.

## Mode Routing

Use **Quick Scan** when the user asks for a fast look, such as "is there
anything like this", "有类似的吗", "quickly check existing tools", or "does this
already exist". Do not write files by default. Return a compact candidate table,
uncertainty, and the next source to check.

Use **Formal Gate** when the user asks for deep research, systematic research,
a full comparison, a report, prior-art map, build-vs-adopt guidance, roadmap
evaluation, due diligence, or whether the direction is worth doing. Write
artifacts under `/tmp` unless the user asks to curate them into the repository.

If ambiguous, infer Quick Scan unless the user mentions report, deep research,
formal evaluation, roadmap, ADR, backlog, due diligence, or decision gate.

## Reference Routing

Read only the references needed for the current mode:

- Brief shape: `references/discovery-brief.md`.
- Target-specific sources: `references/source-routing.md`.
- Query families: `references/query-matrix.md`.
- Coverage confidence: `references/coverage-protocol.md`.
- Source adapters and fallback behavior: `references/search-adapters.md`.
- Technical due-diligence exit criteria: `references/due-diligence-gate.md`.
- Candidate evidence categories: `references/candidate-evidence.md`.
- Recommendation semantics: `references/recommendation-rubric.md`.
- Markdown and JSON output contract: `references/report-contract.md`.
- Positioning and differentiation: `references/positioning-discussion.md`.
- False-confidence blockers: `references/anti-rationalizations.md`.
- Cross-agent execution: `references/cross-agent-protocol.md`.
- Current subskill split rules: `references/skill-pack-routing.md`.
- Safety boundaries: `references/safety.md`.

## Using `project-scout`

For fixture or manual candidates:

```bash
.venv/bin/project-scout report \
  --brief path/to/brief.json \
  --candidates path/to/candidates.json \
  --out-json /tmp/project-scout-report.json \
  --out-md /tmp/project-scout-report.md
```

For a new brief:

```bash
.venv/bin/project-scout init-brief \
  --template skill \
  --out /tmp/prior-art-brief.json
```

For bounded GitHub search:

```bash
.venv/bin/project-scout report \
  --brief path/to/brief.json \
  --github-query "query terms" \
  --github-limit 10 \
  --github-timeout 10 \
  --no-github-readme \
  --out-json /tmp/project-scout-github.json \
  --out-md /tmp/project-scout-github.md
```

For bounded skills registry search:

```bash
.venv/bin/project-scout report \
  --brief path/to/brief.json \
  --skills-query "query terms" \
  --skills-timeout 10 \
  --out-json /tmp/project-scout-skills.json \
  --out-md /tmp/project-scout-skills.md
```

If the engine is unavailable, write a provisional report using
`references/report-contract.md`, mark the missing engine as a process gap, and
avoid high-confidence decisions.

## Red Flags

Stop and downgrade confidence when any of these occur:

- The report implies exhaustive search from bounded queries.
- A failed adapter is omitted from the source log.
- A known candidate is missing without explanation.
- Popularity, stars, install count, SEO rank, or social buzz is treated as adoption proof.
- LLM summaries replace primary-source evidence.
- Candidate-level `Write New` appears.
- Coverage is `Low` but the discussion uses strong adoption or uniqueness language.
- The output mutates roadmaps, ADRs, issues, PRs, or backlog without explicit user request.

## Verification

Before answering Formal Gate completion, verify:

- source log includes concrete sources, queries or URLs, result counts, used counts, status, and errors;
- coverage confidence and blind spots are present;
- known candidates are included or listed as misses;
- `project-scout` JSON and Markdown artifacts exist, or the missing engine is stated;
- recommendation, decision confidence, coverage confidence, and go/review/hold are separated;
- candidate evidence gaps are visible;
- positioning claims cite report evidence and avoid unsupported uniqueness claims;
- draft outputs are under `/tmp` unless the user asked to curate them.

## Exit Criteria

Quick Scan is complete when the answer includes the practical verdict, top
candidates or absence of strong candidates, source uncertainty, and the next
source to check.

Formal Gate is complete when the generated artifact links are provided and the
summary includes:

- top recommendation;
- decision confidence;
- coverage confidence;
- go/review/hold dashboard status and primary action;
- top 3-5 candidates;
- major borrow/adopt/integrate signals;
- major avoid or unknown signals;
- blind spots and next validation step.

Do not push, publish, create issues, open PRs, or edit roadmap/backlog/ADR files
unless the user explicitly asks for that action.
