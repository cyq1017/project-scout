# Milestone 1: Local Prior-Art Gate

Status: Achieved locally
Date: 2026-06-20

## Definition

Milestone 1 means `project-scout` is stable enough to act as a local,
fixture-first prior-art gate before a user starts building, adopting, forking,
or positioning a small project, skill, plugin, tool, product, paper, or
integration.

This milestone is not a crawler platform, hosted service, autonomous agent, or
final decision maker. It is a deterministic CLI/library plus skill source that
turns a brief and bounded candidate set into an auditable report.

## Acceptance Criteria

- Development bootstrap is reliable on the current machine.
- Installed console script works without setting `PYTHONPATH`.
- Source-tree fallback works for recovery and troubleshooting.
- Full pytest suite completes without hanging.
- Wheel install smoke works in a clean virtual environment.
- Reports include deterministic scoring, coverage, source requirements, search
  log, blind spots, decision confidence, and report-level recommendation.
- Reports preserve discovery brief fields and support non-repo candidate kinds
  such as skills, products, papers, plugins, and MCP-style servers.
- Candidate evidence records expose license, maintenance, primary-source,
  integration, pricing, and security unknowns.
- Markdown reports include a first-page positioning brief and decision
  dashboard before raw tables.
- Differentiation support is conservative: commodity features, unique
  combination, claims to avoid, candidate roles, and README positioning draft.
- `prior-art-scout` skill source matches the executable report contract.
- README, HANDOFF, BACKLOG, report schema, sample JSON, and sample Markdown
  reflect the current behavior.
- No push, release, public PR, token storage, or live credential requirement is
  part of the milestone.

## Verified Gates

The current milestone was verified with:

```bash
.venv/bin/python -m pytest
scripts/smoke.sh
.venv/bin/python -m pip wheel . -w /tmp/project-scout-wheelhouse
/tmp/project-scout-wheel-venv/bin/project-scout report \
  --brief tests/fixtures/brief.json \
  --candidates tests/fixtures/github_repos.json \
  --out-json /tmp/project-scout-wheel.json \
  --out-md /tmp/project-scout-wheel.md \
  --generated-at 2026-06-04T00:00:00+00:00
git diff --check
```

## Milestone Boundary

M1 is complete when the project can be handed to another reviewer with this
contract:

- Run bootstrap or use the existing healthy `.venv`.
- Run tests and smoke gates.
- Generate a fixture report.
- Inspect the first page for the positioning brief and decision dashboard.
- Review source coverage and unknown evidence before acting on recommendations.

If those gates pass, the milestone is done even if later product polish remains.

## Deferred To Later Milestones

- Real-world AgentUX formal gate report curated from live search sources.
- More source adapters or richer source profile presets.
- Better candidate ingestion UX for copied web tables or search dumps.
- Optional LLM summarization as an external adapter only.
- Release packaging, public tagging, or README badges.
- Any hosted service, crawler, login flow, issue creation, PR creation, or
  automatic roadmap mutation.

## Next Milestone Candidate

Milestone 2 should focus on one real-world dogfood report, not broad platform
expansion:

- Run a formal gate for a real target such as AgentUX.
- Capture source coverage and blind spots as structured inputs.
- Compare project-scout output against a manual/GPT/Claude review.
- Fix only report usability gaps revealed by that dogfood run.
- Keep all outputs local unless the user explicitly asks to publish them.
