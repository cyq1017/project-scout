# Prior Art Scout MVP Completion Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Finish the `prior-art-scout` MVP so the skill has a real CLI/library path for discovery briefs, known candidates, search logs, coverage confidence, and formal-gate report sections.

**Architecture:** Extend the existing deterministic `project_scout` core rather than replacing it. Add compatibility models for DiscoveryBrief, Candidate source metadata, search log, coverage summary, and decision confidence while preserving existing ProjectBrief fixtures and CLI behavior.

**Tech Stack:** Python dataclasses, argparse CLI, pytest fixture tests, existing Markdown/JSON report writer.

---

### Task 1: Discovery Brief Compatibility

**Files:**
- Modify: `src/project_scout/models.py`
- Modify: `src/project_scout/core.py`
- Test: `tests/test_discovery_brief.py`
- Add fixture: `tests/fixtures/discovery_brief.json`

**Steps:**
1. Write failing tests for `load_brief` accepting a DiscoveryBrief and mapping it to `ProjectBrief`.
2. Verify the test fails because `ProjectBrief.from_dict` ignores discovery fields.
3. Add `DiscoveryBrief` and compatibility mapping.
4. Run the focused test and full test suite.

### Task 2: Search Log And Coverage

**Files:**
- Modify: `src/project_scout/models.py`
- Modify: `src/project_scout/core.py`
- Modify: `src/project_scout/cli.py`
- Test: `tests/test_core_report.py`
- Test: `tests/test_cli.py`

**Steps:**
1. Write failing tests that reports include `decision`, `coverage`, and `search_log`.
2. Verify failure.
3. Add `DecisionSummary`, `CoverageSummary`, `SearchLogEntry`, and CLI-generated log entries for candidates, URLs, GitHub search, known candidate files, and skills registry query attempts.
4. Run focused tests and full tests.

### Task 3: Formal Gate Markdown Sections

**Files:**
- Modify: `src/project_scout/report.py`
- Test: `tests/test_core_report.py`

**Steps:**
1. Write failing tests for required Formal Gate sections: Search Summary, Coverage Matrix, Recommendation And Confidence, Coverage Confidence And Blind Spots.
2. Verify failure.
3. Render the new sections while keeping old sections compatible.
4. Run focused tests and full tests.

### Task 4: Skills Registry Adapter

**Files:**
- Create: `src/project_scout/skills_registry.py`
- Modify: `src/project_scout/cli.py`
- Test: `tests/test_importers.py`
- Test: `tests/test_cli.py`

**Steps:**
1. Write failing tests for parsing `npx skills find` output into candidates without network.
2. Verify failure.
3. Add a parser and optional CLI `--skills-query` adapter using subprocess with timeout; failures become search log entries instead of crashing.
4. Run focused tests and full tests.

### Task 5: Install And Community Docs

**Files:**
- Modify: `README.md`
- Modify: `docs/skill-repository-strategy.md`
- Modify: `BACKLOG.md`

**Steps:**
1. Document local user-level install/copy command.
2. Document that public GitHub release requires explicit approval.
3. Run `quick_validate.py`, `pytest`, and `git diff --check`.
4. Commit.
