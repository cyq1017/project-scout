# Milestone 6: Research Quality Harness

Status: Complete
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
- `package_plugin_integration`: a close adjacent editor/terminal plugin should
  become an integration or fork review path, not a generic market claim.
- `paper_research_target`: a research/paper target should anchor on comparable
  methods and avoid over-claiming against leaderboard-only alternatives.
- `false_positive_write_new_prevention`: weak candidates plus missing known
  candidates should produce Research More rather than a premature Write New.
- `thin_coverage_hold`: failed required source coverage and missing known
  candidates should produce Research More and a hold dashboard state.

## Acceptance Criteria

- At least one benchmark covers a product-positioning case.
- At least one benchmark covers a direct project adoption case.
- At least one benchmark covers package or plugin integration.
- At least one benchmark covers paper or research target comparison.
- At least one benchmark prevents false-positive Write New when coverage is
  incomplete.
- At least one benchmark covers low coverage and hold behavior.
- Each benchmark checks decision recommendation, coverage confidence,
  go/review/hold status, closest comparison anchor, and selected Markdown or
  claims-to-avoid evidence.
- Full pytest suite passes locally.

## Benchmark Summary

| Case | Target shape | Guardrail |
| --- | --- | --- |
| `agentux_terminal_selection` | Product positioning with strong adjacent prior art | Write New remains calibrated and comparison anchors stay visible. |
| `direct_adoption_candidate` | Direct project adoption | High-overlap permissive candidates can recommend Adopt while staying review-gated. |
| `package_plugin_integration` | Package/plugin integration | Close plugin prior art is treated as an adoption or integration review path. |
| `paper_research_target` | Paper/research comparison | Research targets anchor on comparable methods and avoid shallow leaderboard claims. |
| `false_positive_write_new_prevention` | Weak candidate with missing known candidate | Missing known candidates prevent premature Write New. |
| `thin_coverage_hold` | Failed source coverage | Required-source failure produces Research More and hold. |

## Remaining Work

- Add future benchmark cases when real regressions appear in dogfood runs.

## Verification

Run:

```bash
.venv/bin/python -m pytest tests/test_research_quality_harness.py -q
.venv/bin/python -m pytest
```
