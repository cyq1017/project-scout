# Prior Art Scout M4 Skill Pack Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Rework `prior-art-scout` into an agent-skills-style technical due-diligence workflow with concise entry instructions, progressive references, evidence gates, anti-rationalization checks, and a deliberate path toward optional subskills.

**Architecture:** Keep `project-scout` as the deterministic CLI/library engine. Keep `skills/prior-art-scout/SKILL.md` as the primary trigger and workflow router for M4, with detailed search, evidence, positioning, and decision material loaded from one-level `references/` files. Do not split into multiple independently triggered skill folders until forward-tests show that agents reliably need separate entrypoints.

**Tech Stack:** Markdown skill source, `agents/openai.yaml`, Python pytest contract tests, existing `project-scout` CLI/library, local fixture-first validation.

---

## Product Framing

M4 reframes the skill from "prior-art research" to:

```text
pre-build / pre-adopt technical due diligence for build-vs-adopt decisions
```

Chinese shorthand:

```text
开工前技术尽调 / 采用前方案尽调
```

This is not legal, financial, acquisition, or compliance due diligence. It is a
technical evidence gate for questions such as:

- does this already exist?
- what was actually searched?
- which candidates are direct, close adjacent, broad adjacent, or irrelevant?
- what evidence is primary-source verified?
- should the user adopt, integrate, fork, extend, borrow, write new, avoid, or research more?
- what positioning claims are defensible from the evidence?

## Design Principles To Steal From agent-skills

- Process over prose: every section must tell the agent what to do, not merely what to know.
- Progressive disclosure: `SKILL.md` stays short; detailed references load only when needed.
- Verification is non-negotiable: every Formal Gate ends with concrete artifact and evidence checks.
- Anti-rationalization: document common shortcuts agents take and block them explicitly.
- Exit criteria: define when Quick Scan, Formal Gate, and Forward-Test Review are complete.
- Tool-neutral routing: use capabilities first, concrete tools second.

## M4 Scope

M4 updates the existing `prior-art-scout` skill and its references. It does not
create a large public skill marketplace or crawler platform.

M4 includes:

1. Rewrite `SKILL.md` into a concise workflow entrypoint.
2. Add due-diligence framing and anti-rationalization references.
3. Strengthen candidate evidence review.
4. Strengthen build-vs-adopt decision gates.
5. Add tests that prevent the skill from becoming prose-only.
6. Update docs and milestones.
7. Forward-test with one fresh AgentUX-like task after implementation.

M4 excludes:

- broad web crawling;
- token, cookie, account, or browser-session storage;
- live social platform automation by default;
- automatic issue, PR, ADR, roadmap, or backlog mutation;
- LLM-only scoring or unverified claims;
- publishing or pushing without explicit user authorization.

## Subskill Packaging Decision

Do not immediately create five independent skills. Start with one strong skill
and one-level references. Independent subskills should be created only if
forward-tests show one of these problems:

- agents frequently skip a phase because `SKILL.md` is too dense;
- users ask for one phase directly, such as "just evaluate evidence quality";
- cross-agent trigger descriptions become clearer as separate capabilities;
- a phase needs its own scripts, assets, or validation flow.

Target future pack if splitting becomes justified:

```text
skills/
├── prior-art-scout/              # Router and formal gate orchestrator
├── source-coverage-scout/        # Query matrix, source log, coverage gaps
├── candidate-evidence-review/    # License, maintenance, security, cost, integration evidence
├── positioning-differentiator/   # Differentiation, claims to avoid, README positioning
└── build-vs-adopt-gate/          # Adopt / Integrate / Fork / Extend / Borrow / Write New gate
```

For M4, model those future subskills as references inside
`skills/prior-art-scout/references/`.

## Planned File Layout

Current files to keep:

```text
skills/prior-art-scout/
├── SKILL.md
├── agents/openai.yaml
└── references/
    ├── coverage-protocol.md
    ├── cross-agent-protocol.md
    ├── discovery-brief.md
    ├── positioning-discussion.md
    ├── query-matrix.md
    ├── recommendation-rubric.md
    ├── report-contract.md
    ├── safety.md
    ├── search-adapters.md
    └── source-routing.md
```

Add or update:

```text
skills/prior-art-scout/references/
├── anti-rationalizations.md      # Shortcut blockers and rebuttals
├── candidate-evidence.md         # Evidence categories and primary-source review
├── due-diligence-gate.md         # Technical due-diligence framing and exit criteria
└── skill-pack-routing.md         # When to keep one skill vs split into subskills
```

Repo docs:

```text
docs/milestones/m4-skill-pack-due-diligence-gate.md
docs/plans/2026-06-20-prior-art-scout-m4-skill-pack-plan.md
```

Tests:

```text
tests/test_prior_art_scout_skill.py
```

## Task 1: Add M4 Contract Tests

**Files:**

- Modify: `tests/test_prior_art_scout_skill.py`
- Read: `skills/prior-art-scout/SKILL.md`
- Read: `skills/prior-art-scout/references/*.md`

**Step 1: Write failing tests**

Add tests that assert:

- `SKILL.md` links:
  - `references/due-diligence-gate.md`
  - `references/candidate-evidence.md`
  - `references/anti-rationalizations.md`
  - `references/skill-pack-routing.md`
- `SKILL.md` contains agent-skills-style section markers:
  - `Core Process`
  - `Red Flags`
  - `Verification`
  - `Exit Criteria`
- `SKILL.md` still keeps `project-scout` as the deterministic engine boundary.
- No skill reference claims exhaustive search, automatic final decisions, or legal/financial due diligence.
- The new anti-rationalization reference blocks these shortcuts:
  - "no results means no competitors";
  - "stars prove adoption";
  - "LLM summary replaces primary source";
  - "coverage low but recommendation high";
  - "Write New from one weak candidate".

**Step 2: Run test to verify it fails**

```bash
.venv/bin/python -m pytest tests/test_prior_art_scout_skill.py -q
```

Expected: fail because the new references and section markers are not present.

**Step 3: Commit only after green**

Do not commit in this task until Tasks 2-5 make the tests pass.

## Task 2: Rewrite SKILL.md As A Workflow Router

**Files:**

- Modify: `skills/prior-art-scout/SKILL.md`
- Modify if needed: `skills/prior-art-scout/agents/openai.yaml`

**Target shape:**

```markdown
---
name: prior-art-scout
description: Run pre-build and pre-adopt technical due diligence for build-vs-adopt decisions...
---

# Prior Art Scout

## Overview
...

## Core Process
1. Classify mode.
2. Capture brief.
3. Plan coverage.
4. Collect candidates.
5. Normalize evidence.
6. Run project-scout.
7. Interpret decision.
8. Verify outputs.

## Mode Routing
...

## Reference Routing
...

## Red Flags
...

## Verification
...

## Exit Criteria
...
```

**Implementation notes:**

- Keep the body under 500 lines.
- Move explanations into references instead of expanding `SKILL.md`.
- Keep Quick Scan chat-only by default.
- Keep Formal Gate artifact-based.
- Keep `/tmp` as default output location for draft artifacts.
- Use new M3 options in live commands:
  - `--github-timeout`
  - `--no-github-readme`
  - `--skills-timeout`

**Run:**

```bash
.venv/bin/python -m pytest tests/test_prior_art_scout_skill.py -q
```

Expected: still fail until new references exist.

## Task 3: Add Due-Diligence Gate Reference

**Files:**

- Create: `skills/prior-art-scout/references/due-diligence-gate.md`
- Modify if needed: `skills/prior-art-scout/references/report-contract.md`

**Content requirements:**

Include:

- definition of technical due diligence;
- out-of-scope legal/financial/compliance disclaimers;
- Quick Scan exit criteria;
- Formal Gate exit criteria;
- claim-scope language:

```text
No exhaustive-search claim is made. Conclusions apply only to the recorded
sources, queries, dates, access constraints, and verification steps.
```

- required Formal Gate artifacts:
  - Discovery Brief;
  - source log;
  - query matrix or query family notes;
  - structured candidates;
  - `project-scout` JSON;
  - Markdown report;
  - coverage confidence;
  - decision dashboard;
  - blind spots;
  - next validation steps.

**Run:**

```bash
.venv/bin/python -m pytest tests/test_prior_art_scout_skill.py -q
```

Expected: fewer missing-reference failures.

## Task 4: Add Candidate Evidence Reference

**Files:**

- Create: `skills/prior-art-scout/references/candidate-evidence.md`
- Modify if needed: `skills/prior-art-scout/references/recommendation-rubric.md`
- Modify if needed: `docs/report-schema.md`

**Content requirements:**

Define evidence categories:

- primary source URL;
- license;
- maintenance/activity;
- integration boundary;
- cost/pricing;
- security/privacy/data handling;
- platform/runtime constraints;
- community/adoption signal;
- fit to must-have requirements;
- mismatch/exclusion evidence.

Define evidence statuses:

```text
known | unknown | conflicting | not_applicable
```

Define source quality:

```text
primary | official_secondary | community | inferred | unknown
```

State that adoption recommendations require primary-source review for the
categories that matter to the decision.

**Run:**

```bash
.venv/bin/python -m pytest tests/test_prior_art_scout_skill.py -q
```

Expected: candidate-evidence checks pass.

## Task 5: Add Anti-Rationalizations Reference

**Files:**

- Create: `skills/prior-art-scout/references/anti-rationalizations.md`
- Modify: `skills/prior-art-scout/SKILL.md`

**Content shape:**

Use a compact table:

```markdown
| Rationalization | Why it is wrong | Required response |
| --- | --- | --- |
| No results means no competitors | Search coverage is bounded and source-dependent | Record blind spot and say Research More |
```

Must include at least these rows:

- No results means no competitors.
- Stars prove adoption fit.
- LLM summary replaces primary source.
- One high-score candidate means Adopt.
- Coverage Low but recommendation High is acceptable.
- Write New can be attached to a candidate.
- A web result can stand in for manual known-candidate coverage.
- A failed adapter can be ignored if another source worked.

**Run:**

```bash
.venv/bin/python -m pytest tests/test_prior_art_scout_skill.py -q
```

Expected: anti-rationalization checks pass.

## Task 6: Add Skill-Pack Routing Reference

**Files:**

- Create: `skills/prior-art-scout/references/skill-pack-routing.md`
- Modify: `skills/prior-art-scout/SKILL.md`
- Modify: `docs/skill-repository-strategy.md`

**Content requirements:**

Document the current M4 decision:

- keep one public trigger skill for now;
- use references as internal phase modules;
- split later only if forward-tests show trigger or context problems.

Define future optional subskills:

| Proposed subskill | Trigger | Owns | Should not own |
| --- | --- | --- | --- |
| `source-coverage-scout` | user asks only about search coverage | sources, queries, source log | final adoption decision |
| `candidate-evidence-review` | user asks whether candidates are trustworthy | evidence quality | discovery breadth |
| `positioning-differentiator` | user asks what is unique or defensible | positioning, claims to avoid | source collection |
| `build-vs-adopt-gate` | user asks whether to build or adopt | decision gate | raw search |

Add split criteria:

- two forward-tests show agents skip the phase in a monolithic skill;
- user asks for the phase as a standalone task three or more times;
- the phase needs its own scripts or assets;
- trigger description is clearer than the parent skill.

Add do-not-split criteria:

- only for aesthetics;
- only because there are many references;
- if splitting weakens evidence continuity;
- if it causes agents to skip `project-scout` engine output.

**Run:**

```bash
.venv/bin/python -m pytest tests/test_prior_art_scout_skill.py -q
```

Expected: all new skill contract tests pass.

## Task 7: Update Milestone And User Docs

**Files:**

- Create: `docs/milestones/m4-skill-pack-due-diligence-gate.md`
- Modify: `README.md`
- Modify: `HANDOFF.md`
- Modify: `BACKLOG.md`

**Milestone acceptance criteria:**

- `prior-art-scout` uses agent-skills-style process sections.
- Formal Gate has due-diligence exit criteria.
- Anti-rationalizations are explicit and referenced.
- Candidate evidence review is explicit and primary-source oriented.
- Skill-pack routing explains why M4 remains one skill plus references.
- Future subskills are designed but not created unless justified.
- Tests and smoke gates pass.

**README wording:**

Add this positioning:

```text
project-scout is a local-first prior-art and technical due-diligence gate for build-vs-adopt decisions.
```

Clarify:

- "technical due diligence" means evidence-backed technical review;
- it is not legal, financial, acquisition, compliance, or exhaustive market diligence.

**Run:**

```bash
.venv/bin/python -m pytest tests/test_prior_art_scout_skill.py -q
git diff --check
```

Expected: pass.

## Task 8: Forward-Test Prompt

**Files:**

- Create: `docs/plans/2026-06-20-m4-forward-test-prompt.md`

**Prompt requirements:**

Write a fresh-agent prompt that asks another agent to use:

```text
skills/prior-art-scout
```

on a realistic target, preferably AgentUX or another current product idea, but
do not include expected findings.

Require outputs under:

```text
/tmp/project-scout-m4-forward-<agent>-<timestamp>
```

Require artifacts:

- source log;
- query family notes;
- candidate JSON;
- `project-scout` report JSON;
- Markdown report;
- positioning discussion;
- evidence-gap checklist;
- self-review against M4 milestone.

**Run:**

```bash
git diff --check
```

Expected: pass.

## Task 9: Full Verification

**Files:**

- All changed files.

**Run:**

```bash
.venv/bin/python -m pytest
scripts/smoke.sh
git diff --check
```

Expected:

- pytest passes;
- smoke writes `/tmp/project-scout-entrypoint.*` and `/tmp/project-scout-smoke.*`;
- diff check exits 0.

If any scripts are added, run them directly with representative inputs.

## Task 10: Commit

**Files:**

- Stage only M4 implementation files.
- Do not stage `docs/plans/project-scout-adjustment-plan.md` unless the user explicitly asks to formalize that GPT Pro draft.

**Run:**

```bash
git status --short --branch
git diff --stat
git diff --check
git add <M4 files only>
git diff --cached --stat
git commit -m "Refine prior-art-scout as due diligence skill"
```

Expected:

- one focused local commit;
- repository remains local-only;
- no push.

## Completion Criteria

M4 is complete when:

- `prior-art-scout` reads like an executable workflow, not a reference essay;
- references are one level deep and loaded by need;
- technical due-diligence framing is clear and bounded;
- anti-rationalizations block common false confidence paths;
- candidate evidence review separates primary facts from inferred summaries;
- subskill split rules are documented but not prematurely implemented;
- tests and smoke gates pass;
- a local commit records the work.

## After M4

If M4 forward-tests show the parent skill still causes confusion, start M5:

```text
M5: Prior-Art Scout Skill Pack Split
```

M5 should create at most one new subskill first, probably
`candidate-evidence-review`, because it has the clearest standalone trigger and
the lowest risk of weakening source coverage continuity.
