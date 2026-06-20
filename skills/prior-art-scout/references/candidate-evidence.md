# Candidate Evidence Review

Use this reference after candidates are found and before interpreting
recommendations. The goal is to separate verified facts from assumptions in the
`project-scout` report.

## Evidence Categories

For each material candidate, record what is known, unknown, or conflicting:

| Category | What To Check | Typical Source |
| --- | --- | --- |
| Primary source URL | canonical repo, docs, paper, product page, or registry listing | primary |
| License or terms | license, commercial terms, redistribution limits | primary |
| Maintenance/activity | recent commits, releases, changelog, issue activity, docs freshness | primary or official secondary |
| Integration boundary | API, CLI, plugin interface, MCP tools, data flow, runtime requirements | primary |
| Cost/pricing | hosted pricing, paid tiers, infrastructure cost, usage limits | primary |
| Security/privacy/data handling | auth, token handling, local/remote execution, data retention | primary |
| Platform/runtime constraints | OS, terminal, IDE, browser, language, package ecosystem | primary |
| Community/adoption signal | stars, installs, mentions, issues, posts | community |
| Fit to must-have requirements | direct support for the brief's required workflow | primary plus report overlap |
| Mismatch/exclusion evidence | conflicts with exclusions, wrong audience, wrong workflow | primary or inferred |

## Evidence Status

Use these statuses in notes and report discussion:

```text
known | unknown | conflicting | not_applicable
```

- `known`: supported by a cited source or user-provided artifact.
- `unknown`: material fact was not found or source was unavailable.
- `conflicting`: sources disagree or candidate docs are inconsistent.
- `not_applicable`: category is not relevant to this decision.

## Source Quality

Use these source quality labels:

```text
primary | official_secondary | community | inferred | unknown
```

- `primary`: canonical repo, official docs, registry listing, product page, paper, or user-provided local artifact.
- `official_secondary`: vendor blog, changelog, release note, or official comparison page.
- `community`: Reddit, HN, forum, social, third-party review, package discussion, issue comments.
- `inferred`: derived from metadata, naming, topics, or LLM summary.
- `unknown`: no source quality can be established.

## Adoption Evidence Gate

Do not recommend adoption or integration strongly unless primary-source evidence
covers the categories material to the decision.

At minimum, adoption-oriented recommendations need:

- primary source URL known;
- license or terms known;
- maintenance/activity known enough for the intended use;
- integration boundary known;
- material security/privacy/cost constraints known or explicitly not relevant.

If those are missing, use `Research More`, `Borrow`, or `Monitor` instead of
strong adoption language.

## How To Use With project-scout

`project-scout` emits structured `evidence_records` for license, maintenance,
primary source, integration, and pricing/security. Treat those records as the
starting checklist. Add human review notes for categories the engine cannot
verify automatically.

Do not let README summaries, search snippets, LLM summaries, stars, or install
counts replace primary-source review.

## Output Pattern

For top candidates, summarize evidence gaps compactly:

```text
Candidate: example/tool
Known: primary URL, license, runtime
Unknown: pricing/security, integration cost
Risk: API shape is documented but data handling is unclear
Next check: read official security and integration docs
```
