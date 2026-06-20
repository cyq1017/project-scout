# Milestone 6: Research Quality Harness

Status: In Progress
Date: 2026-06-21

## Definition

Milestone 6 means `project-scout` has repeatable quality checks for prior-art
and technical due-diligence reports. The goal is not to prove that search is
exhaustive. The goal is to catch obvious decision-quality regressions before a
report is trusted by a user or reviewer.

The harness stays fixture-first and deterministic. It does not add live crawler
behavior, LLM judging, login flows, or automatic final decisions.

## Current Benchmark Cases

The benchmark fixtures live under `tests/quality_cases`:

- `agentux_terminal_selection`: strong close-adjacent product prior art should
  produce a calibrated Write New decision with explicit comparison anchors and
  claims to avoid.
- `direct_adoption_candidate`: a high-overlap permissive Python CLI candidate
  should produce an Adopt recommendation, but still require human review for
  unknown integration/security evidence.
- `thin_coverage_hold`: failed required source coverage and missing known
  candidates should produce Research More and a hold dashboard state.

## Acceptance Criteria

- At least one benchmark covers a product-positioning case.
- At least one benchmark covers a direct project adoption case.
- At least one benchmark covers low coverage and hold behavior.
- Each benchmark checks decision recommendation, coverage confidence,
  go/review/hold status, closest comparison anchor, and selected Markdown or
  claims-to-avoid evidence.
- Full pytest suite passes locally.

## Remaining Work

- Add package/plugin adoption benchmark cases.
- Add paper/research target benchmark cases.
- Add false-positive Write New prevention cases.
- Add a small markdown summary table that explains what each benchmark guards.

## Verification

Run:

```bash
.venv/bin/python -m pytest tests/test_research_quality_harness.py -q
.venv/bin/python -m pytest
```
