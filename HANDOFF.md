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

When using the checked-in local `.venv` from a path containing spaces, Python 3.14 may mark editable `.pth` files hidden on macOS. If imports fail only inside that local venv, run:

```bash
chflags -R nohidden .venv/lib/python*/site-packages
```

Fixture report generation should use:

```bash
project-scout report \
  --brief tests/fixtures/brief.json \
  --candidates tests/fixtures/github_repos.json \
  --out-json project-scout-report.json \
  --out-md docs/research/2026-05-prior-art-map.md
```

If `--out-md` is omitted, the CLI writes to `docs/research/YYYY-MM-prior-art-map.md` for the current UTC month.

Live GitHub search uses unauthenticated requests for both repository search and best-effort README summaries. Rate-limit or README failures leave `readme_summary` empty rather than failing the whole report.
