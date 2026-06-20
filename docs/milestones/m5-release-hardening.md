# Milestone 5: Release Hardening

Status: In Progress
Date: 2026-06-20

## Definition

Milestone 5 means `project-scout` is stable enough for another user to clone,
install, verify, and run as a local-first CLI/library without relying on this
machine's editable install state.

M5 keeps the project small: it hardens packaging, CI coverage, report safety,
and public examples. It does not add crawler behavior, login flows, token
storage, hosted services, or automatic final decisions.

## Acceptance Criteria

- Full pytest suite passes locally.
- Fixture smoke covers the installed console script and source-tree fallback.
- Wheel install smoke passes from outside the repository.
- CI covers Linux and macOS across the supported Python range.
- Markdown reports do not leak local absolute paths in rendered prose/tables.
- Markdown candidate links only render safe `http` or `https` URLs.
- README and handoff docs describe the reliable install and verification path.
- Public examples contain no personal paths, raw result dumps, credentials, or
  private artifacts.

## Completed In This Slice

- Markdown report rendering redacts local absolute paths.
- Unsafe candidate URL schemes render as `about:blank`.
- Regression tests cover both release-safety behaviors.
- CI matrix covers Python 3.10, 3.11, 3.12, and 3.13 on Linux and macOS.
- `scripts/wheel-smoke.sh` verifies wheel-installed console-script behavior
  from outside the repository.

## Remaining Work

- Audit curated public examples for personal paths and private artifacts.
- Re-run full local verification after each release-hardening slice.

## Verification

Run:

```bash
.venv/bin/python -m pytest
scripts/smoke.sh
scripts/wheel-smoke.sh
git diff --check
```

For this slice, the targeted regression gate is:

```bash
.venv/bin/python -m pytest \
  tests/test_core_report.py::test_render_markdown_redacts_local_paths_from_source_errors \
  tests/test_core_report.py::test_render_markdown_replaces_unsafe_candidate_link_urls -q
```
