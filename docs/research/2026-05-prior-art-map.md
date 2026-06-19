# project-scout Prior-Art Map

Generated: 2026-05-24T00:00:00Z

## Executive Summary

Reviewed 3 candidate projects. Top recommendation signal: **Fork**. Decision confidence: **Medium**. Coverage confidence: **Medium**.

## Search Summary

| Source | Query | Results | Used | Status | Notes |
| --- | --- | ---: | ---: | --- | --- |
| manual | tests/fixtures/github_repos.json | 3 | 3 | ok |  |

## Source Requirements

| Source | Required |
| --- | --- |
| manual | yes |
| github | yes |
| web | yes |
| skills | no |

## Coverage Matrix

| Source | Status | Used | Notes |
| --- | --- | ---: | --- |
| manual | ok | 3 |  |

## Similar Projects

| Project | Kind | Stars | Updated | License | Language | Score | Recommendation |
| --- | --- | ---: | --- | --- | --- | ---: | --- |
| [sample/prior-art-cli](https://github.com/sample/prior-art-cli) | repo | 128 | 2026-05-01T09:15:00Z | MIT | Python | 0.760 | Fork |
| [ecosyste-ms/repos](https://github.com/ecosyste-ms/repos) | repo | 2100 | 2026-04-12T10:30:00Z | AGPL-3.0 | Ruby | 0.119 | Ignore |
| [octobox/octobox](https://github.com/octobox/octobox) | repo | 4700 | 2025-12-01T08:00:00Z | AGPL-3.0 | Ruby | 0.069 | Ignore |

## Overlap Matrix

| Project | Keywords | Stack | Users | Exclusions | Score |
| --- | ---: | ---: | ---: | ---: | ---: |
| sample/prior-art-cli | 3 | 4 | 0 | 0 | 0.760 |
| ecosyste-ms/repos | 0 | 1 | 0 | 0 | 0.119 |
| octobox/octobox | 0 | 0 | 0 | 0 | 0.069 |

## What To Borrow

- sample/prior-art-cli: borrow evidence around competitive analysis, github search, prior art, cli, json, markdown, python, analysis, art, competitive, github, prior.

## What To Avoid

- ecosyste-ms/repos: low overlap in available metadata.
- octobox/octobox: low overlap in available metadata.

## Recommendation And Confidence

- Recommendation: **Fork**.
- Decision confidence: **Medium**.
- Rationale: sample/prior-art-cli has the strongest current score (0.760).
- Rationale: Recommendation is based on evidence: competitive analysis, github search, prior art, cli, json, markdown, python, analysis, art, competitive, github, prior.
- Confidence reason: 3 candidates compared.
- Confidence reason: Metadata is deterministic but may need manual source verification.
- Confidence reason: Coverage confidence caps decision confidence at Medium.
- Confidence reason: One or more adoption evidence records are still unknown.
- Treat this as research input, not an automatic decision.

## Coverage Confidence And Blind Spots

- Coverage confidence: **Medium**.
- Stop reason: Compared available candidates after recorded source collection.
- Blind spot: Web and community sources were not covered unless supplied manually.
- Blind spot: GitHub repository search was not covered unless supplied manually.
- Blind spot: Skills registry was not covered unless supplied manually.
- Blind spot: Required source not satisfied: github.
- Blind spot: Required source not satisfied: web.

## Differentiation Map

- Similarity cluster: High similarity: sample/prior-art-cli.
- Similarity cluster: Low relevance: ecosyste-ms/repos, octobox/octobox.
- Commodity feature: github
- Commodity feature: analysis
- Commodity feature: competitive
- Commodity feature: competitive analysis
- Commodity feature: github api
- Commodity feature: github search
- Commodity feature: json
- Commodity feature: markdown
- Unique combination: Differentiate through the combined workflow, not a single feature: prior art; competitive analysis; github search; roadmap; python.
- Defensible positioning: Frame differentiation as a combination claim, not a uniqueness claim.
- Defensible positioning: Position project-scout around the project workflow it enables; compare directly against the closest recorded candidates.
- Defensible positioning: Use sample/prior-art-cli as the first comparison anchor.
- Claim to avoid: Do not position around crawler platform.
- Claim to avoid: Do not position around stored tokens.
- Claim to avoid: Do not position around autonomous agent.
- Claim to avoid: Do not claim competitive analysis is unique without primary-source evidence.
- Claim to avoid: Do not claim github api is unique without primary-source evidence.
- Claim to avoid: Do not claim github search is unique without primary-source evidence.
- Borrow / integrate / compete: Borrow from sample/prior-art-cli: inspect competitive analysis, github search, prior art, cli before claiming differentiation.
- Borrow / integrate / compete: Borrow from ecosyste-ms/repos: inspect github api, github before claiming differentiation.
- Borrow / integrate / compete: Borrow from octobox/octobox: inspect github before claiming differentiation.
- README positioning draft: project-scout is a project for staff engineers, technical founders that combines prior art, competitive analysis, github search. It should be evaluated against recorded prior art and does not claim exhaustive discovery. It is not crawler platform.

## Differentiation Is Not Enough: Useful Positioning

- Position around the workflow decision this tool enables: evidence-backed build/adopt/fork/plugin choices before roadmap commitment.
- Compare explicitly against: sample/prior-art-cli, ecosyste-ms/repos, octobox/octobox.

## Risks And Unknowns

- ecosyste-ms/repos: AGPL license may limit direct adoption.
- octobox/octobox: AGPL license may limit direct adoption.

## Suggested ADR / Backlog Updates

- ADR: Record why Fork is the current recommendation for sample/prior-art-cli.
- Backlog: Add manual review tasks for license, maintenance activity, and integration cost.
- Backlog: Track borrowed ideas separately from differentiating product decisions.
