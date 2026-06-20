# Milestone 4: Skill-Pack Due-Diligence Gate

Status: Complete
Date: 2026-06-20

## Definition

Milestone 4 means `prior-art-scout` is an agent-skills-style executable
workflow for pre-build and pre-adopt technical due diligence. It keeps
`project-scout` as the deterministic engine, keeps `SKILL.md` concise, and uses
one-level references for source coverage, candidate evidence, positioning,
decision gating, safety, and anti-rationalization rules.

M4 does not split the skill into multiple public subskills. It documents the
future split criteria and keeps one parent skill in charge until forward-tests
show a real trigger or context-loading problem.

## Acceptance Criteria

- `prior-art-scout` uses agent-skills-style process sections:
  - Core Process;
  - Mode Routing;
  - Reference Routing;
  - Red Flags;
  - Verification;
  - Exit Criteria.
- Formal Gate has technical due-diligence exit criteria.
- Candidate evidence review separates primary facts from inferred or community
  signals.
- Anti-rationalizations explicitly block false-confidence shortcuts.
- Skill-pack routing explains why M4 remains one skill plus references.
- Future subskills are designed but not created unless justified by
  forward-tests or repeated standalone use.
- Tests verify the skill contract and reference links.
- Standard local verification passes.

## Skill References Added

```text
skills/prior-art-scout/references/due-diligence-gate.md
skills/prior-art-scout/references/candidate-evidence.md
skills/prior-art-scout/references/anti-rationalizations.md
skills/prior-art-scout/references/skill-pack-routing.md
```

## Planned Future Subskills

These are not created in M4:

| Proposed subskill | Purpose |
| --- | --- |
| `source-coverage-scout` | Source coverage, query matrix, source log, coverage gaps |
| `candidate-evidence-review` | Primary-source evidence quality and adoption readiness |
| `positioning-differentiator` | Defensible positioning and claims to avoid |
| `build-vs-adopt-gate` | Final decision gate after candidate and evidence review |

## Verification

Run:

```bash
.venv/bin/python -m pytest
scripts/smoke.sh
git diff --check
```

For skill-only edits, the targeted contract gate is:

```bash
.venv/bin/python -m pytest tests/test_prior_art_scout_skill.py -q
```

## Forward-Test Gate

Use:

```text
docs/plans/2026-06-20-m4-forward-test-prompt.md
```

Forward-tests should ask a fresh agent to use `skills/prior-art-scout` on a real
prior-art task without giving expected findings. Review the produced source log,
candidate evidence, `project-scout` artifacts, positioning discussion, and
self-review against this milestone.

## Completion Boundary

M4 is complete when the skill contract, references, docs, and verification pass.
It does not require running the forward-test immediately, and it does not
authorize pushing, publishing, registry submission, or public promotion.
