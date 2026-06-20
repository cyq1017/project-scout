# Milestone 7: Skill Experience Gate

Status: Complete
Date: 2026-06-21

## Definition

Milestone 7 means `prior-art-scout` is usable as an agent-facing skill, not just
a local CLI wrapper. Another agent should be able to trigger the skill, choose
Quick Scan or Formal Gate, hand work to a reviewer, and return a stable final
answer shape without relying on hidden context from this repository session.

M7 keeps one public skill. It does not split into multiple subskills until real
forward-tests show that separate triggers are necessary.

## Acceptance Criteria

- `SKILL.md` keeps a concise workflow router and one-level reference routing.
- `references/response-contract.md` defines Quick Scan and Formal Gate final
  chat shapes.
- `references/prompt-packs.md` provides reusable Quick Scan Prompt, Formal Gate
  Prompt, and Reviewer Prompt handoffs.
- `tests/quality_cases` exists as a fixture quality harness for decision
  calibration.
- `quick_validate.py` passes for `skills/prior-art-scout`.
- Full pytest suite passes locally.

## Skill Experience Contract

| Surface | Contract |
| --- | --- |
| Trigger | Frontmatter describes prior-art, build-vs-adopt, competitive research, technical due-diligence, and positioning use cases. |
| Mode choice | `SKILL.md` routes ambiguous asks to Quick Scan unless the user asks for report/deep/formal/due-diligence work. |
| Prompt handoff | `references/prompt-packs.md` gives copyable prompts for quick scan, formal gate, and reviewer handoff. |
| Final answer | `references/response-contract.md` separates artifact paths, recommendation, decision confidence, coverage confidence, blind spots, and next validation. |
| Quality check | `tests/quality_cases` protects decision behavior across direct, adjacent, low-coverage, plugin, paper, and false-positive Write New scenarios. |

## Verification

Run:

```bash
.venv/bin/python ${HOME}/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/prior-art-scout
.venv/bin/python -m pytest tests/test_prior_art_scout_skill.py -q
.venv/bin/python -m pytest
```
