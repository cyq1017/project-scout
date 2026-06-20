# Prior Art Scout M2 Skill Quality Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Improve `prior-art-scout` from an engine-backed reporting skill into a repeatable cross-agent discovery and positioning workflow.

**Architecture:** Keep `SKILL.md` concise and move detailed search, discussion, and cross-agent rules into one-level `references/` files. Keep deterministic scoring/reporting in the `project-scout` CLI/library; the skill orchestrates source access, candidate preparation, discussion quality, and engine invocation.

**Tech Stack:** Markdown skill references, Python pytest for lightweight contract checks, existing `project-scout` CLI/library, fixture-first local validation.

---

## Milestone Scope

M2 is a skill-quality milestone, not a crawler or hosted-service milestone.

It improves three quality surfaces:

1. Search quality through source profiles, query matrices, evidence discipline, and source logs.
2. Discussion quality through positioning, critique, improvement, and next-validation rubrics.
3. Cross-agent stability through capability-first instructions, engine-backed report generation, and forward-test prompts.

## Non-Goals

- Do not add broad crawler behavior.
- Do not add token storage, login flows, hosted services, or account automation.
- Do not replace deterministic report generation with LLM-only scoring.
- Do not publish, push, tag, or release unless explicitly authorized.

## Task 1: Add Skill Contract Tests

**Files:**
- Create: `tests/test_prior_art_scout_skill.py`
- Read: `skills/prior-art-scout/SKILL.md`
- Read: `skills/prior-art-scout/references/*.md`

**Step 1: Write failing tests**

Add tests that assert:

- `SKILL.md` links every required M2 reference.
- Required references exist:
  - `query-matrix.md`
  - `positioning-discussion.md`
  - `cross-agent-protocol.md`
- `SKILL.md` still instructs agents to use `project-scout` CLI/library for deterministic scoring and report generation.
- No M2 reference tells the agent to claim exhaustive search or make automatic final decisions.

**Step 2: Run test to verify it fails**

```bash
.venv/bin/python -m pytest tests/test_prior_art_scout_skill.py -q
```

Expected: fail because the new references do not exist yet.

**Step 3: Implement minimal references and SKILL links**

Create the three references and add concise routing links in `SKILL.md`.

**Step 4: Run test to verify it passes**

```bash
.venv/bin/python -m pytest tests/test_prior_art_scout_skill.py -q
```

Expected: pass.

**Step 5: Commit**

```bash
git add tests/test_prior_art_scout_skill.py skills/prior-art-scout/SKILL.md skills/prior-art-scout/references/query-matrix.md skills/prior-art-scout/references/positioning-discussion.md skills/prior-art-scout/references/cross-agent-protocol.md
git commit -m "Add prior-art-scout skill quality references"
```

## Task 2: Search Quality Reference

**Files:**
- Create/modify: `skills/prior-art-scout/references/query-matrix.md`
- Modify if needed: `skills/prior-art-scout/references/source-routing.md`
- Modify if needed: `skills/prior-art-scout/references/coverage-protocol.md`

**Steps:**

1. Define a query matrix with name, synonym, ecosystem, shape, problem, competitor, negative, and community/pain queries.
2. Add target-specific examples for `skill`, `plugin`, `product`, `mcp_server`, `paper`, and `market_opportunity`.
3. Add quality gates:
   - known candidates must be searched directly;
   - at least one synonym/shape expansion round for Quick Scan;
   - at least two expansion/snowball rounds for Formal Gate;
   - required source failures become blind spots, not negative evidence.
4. Keep this reference capability-first and tool-neutral.
5. Run targeted tests from Task 1.

## Task 3: Discussion Quality Reference

**Files:**
- Create/modify: `skills/prior-art-scout/references/positioning-discussion.md`
- Modify if needed: `skills/prior-art-scout/references/recommendation-rubric.md`

**Steps:**

1. Define the discussion layer after report generation.
2. Split discussion outputs into:
   - direct/close/broad adjacent interpretation;
   - unique combination;
   - claims to avoid;
   - borrow/integrate/compete guidance;
   - next validation step;
   - counterargument or critique pass.
3. Add anti-patterns:
   - uniqueness claims without primary evidence;
   - generic "AI wrapper" positioning;
   - treating popularity as product fit;
   - turning `review` into automatic `go`.
4. Require discussion to cite report fields, candidate evidence, and blind spots.
5. Run targeted tests from Task 1.

## Task 4: Cross-Agent Protocol Reference

**Files:**
- Create/modify: `skills/prior-art-scout/references/cross-agent-protocol.md`
- Modify if needed: `skills/prior-art-scout/references/search-adapters.md`
- Modify if needed: `docs/patterns/cross-agent-skill-compatibility.md`

**Steps:**

1. Define capability names before tool names.
2. Require agents to degrade unavailable capabilities into source-log entries or blind spots.
3. Require agents to prepare structured candidates and then call the CLI engine when available.
4. Define "do not hand-write the deterministic report unless the engine is unavailable."
5. Add forward-test prompts for Codex, Claude, and GPT-style agents.
6. Run targeted tests from Task 1.

## Task 5: Dogfood Prompt And Acceptance Packet

**Files:**
- Create: `docs/plans/2026-06-20-agentux-dogfood-prompt.md`
- Create or update: `docs/milestones/m2-skill-quality-gate.md`

**Steps:**

1. Write a fresh prompt for a separate agent to run `prior-art-scout` on AgentUX.
2. The prompt must include the target definition but not the expected answer.
3. Require generated artifacts under `/tmp` unless the user asks to curate them.
4. Define acceptance:
   - source log present;
   - query matrix applied;
   - known candidates included or marked missing;
   - CLI-generated report used when available;
   - discussion cites evidence and blind spots;
   - no unsupported uniqueness claim.
5. Commit.

## Task 6: Full Verification

**Files:**
- All changed files.

**Steps:**

1. Run:

```bash
.venv/bin/python -m pytest
scripts/smoke.sh
git diff --check
```

2. Optional packaging gate when code changes or install docs change:

```bash
rm -rf /tmp/project-scout-wheelhouse /tmp/project-scout-wheel-venv
.venv/bin/python -m pip wheel . -w /tmp/project-scout-wheelhouse
python3 -m venv /tmp/project-scout-wheel-venv
/tmp/project-scout-wheel-venv/bin/python -m pip install /tmp/project-scout-wheelhouse/project_scout-*.whl
/tmp/project-scout-wheel-venv/bin/project-scout report \
  --brief tests/fixtures/brief.json \
  --candidates tests/fixtures/github_repos.json \
  --out-json /tmp/project-scout-wheel.json \
  --out-md /tmp/project-scout-wheel.md \
  --generated-at 2026-06-04T00:00:00+00:00
```

3. Commit with a focused message.

## Completion Criteria

M2 is ready for external review when:

- The skill tells agents how to search, discuss, and degrade across tool availability.
- The deterministic engine remains the reporting source of truth.
- At least one forward-test prompt exists for AgentUX.
- The full local verification gate passes.
- The repo still has no crawler, hosted service, token storage, or automatic roadmap mutation.
