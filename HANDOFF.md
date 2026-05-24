# HANDOFF

## Current State

`project-scout` is being initialized as an independent local-first Python CLI/library for prior-art and competitive-map reports.

## Working Agreements

- Keep implementation small and test-driven.
- Commit in small phases.
- Do not push.
- Prefer fixture tests over live network tests.

## Verification

Primary check:

```bash
pytest
```

Fixture report generation should use:

```bash
project-scout report \
  --brief tests/fixtures/brief.json \
  --candidates tests/fixtures/github_repos.json \
  --out-json project-scout-report.json \
  --out-md docs/research/2026-05-prior-art-map.md
```
