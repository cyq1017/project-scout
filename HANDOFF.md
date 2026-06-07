# HANDOFF

## Current State

`project-scout` is an independent local-first Python CLI/library plus skill
source repository for prior-art and competitive-map reports.

The public source repo is:

```text
https://github.com/cyq1017/project-scout
```

Do not push, publish releases, or open PRs unless the user explicitly asks in
the current task.

## Working Agreements

- Keep implementation small and test-driven.
- Commit in small phases.
- Do not push.
- Prefer fixture tests over live network tests.
- Keep reusable experience in repo-level `docs/`; promote only execution-time
  guidance into `skills/*/references/`.

## Verification

Recommended local bootstrap:

```bash
scripts/bootstrap-dev.sh
```

This creates the real venv under
`${XDG_CACHE_HOME:-$HOME/.cache}/project-scout/venv` by default, links it at
`.venv`, installs `.[dev]`, and runs `scripts/smoke.sh`.

Primary test gate:

```bash
.venv/bin/python -m pytest
```

`scripts/smoke.sh` is the install/entrypoint gate. The pytest suite covers the
library behavior and includes a regression test that invokes
`.venv/bin/project-scout` without `PYTHONPATH`.

Fixture smoke generation after a healthy editable install should use the
console script. This command is also part of `scripts/smoke.sh`:

```bash
.venv/bin/project-scout report \
  --brief tests/fixtures/brief.json \
  --candidates tests/fixtures/github_repos.json \
  --out-json /tmp/project-scout-entrypoint.json \
  --out-md /tmp/project-scout-entrypoint.md \
  --generated-at 2026-06-04T00:00:00+00:00
```

For local recovery or import-path troubleshooting, use the source-tree fallback
path. This command is also part of `scripts/smoke.sh`:

```bash
PYTHONPATH=src .venv/bin/python -m project_scout.cli report \
  --brief tests/fixtures/brief.json \
  --candidates tests/fixtures/github_repos.json \
  --out-json /tmp/project-scout-smoke.json \
  --out-md /tmp/project-scout-smoke.md \
  --generated-at 2026-06-04T00:00:00+00:00
```

Run `scripts/smoke.sh` when checking both paths together.

If `--out-md` is omitted, the CLI writes to `docs/research/YYYY-MM-prior-art-map.md` for the current UTC month.

Known macOS/iCloud editable-install issue:

- If `.venv/bin/project-scout` fails with `ModuleNotFoundError: No module named
  'project_scout'`, rebuild `.venv` with Python 3.12 or 3.13 first by running
  `scripts/bootstrap-dev.sh`.
- If pytest import hangs, inspect `.venv/lib/python*/site-packages` with
  `ls -lO`; hidden/dataless flags on editable install files are suspect.
- `scripts/bootstrap-dev.sh` avoids this by keeping the real venv outside the
  synced checkout and linking it at `.venv`.
- If hidden/dataless flags keep recurring in other generated files, move the
  checkout outside an iCloud-synced folder.

Live GitHub search uses unauthenticated requests for both repository search and best-effort README summaries. Rate-limit or README failures leave `readme_summary` empty rather than failing the whole report.

Experience library entry points:

- `docs/patterns/skill-experience-library.md`
- `docs/patterns/search-routing-pattern.md`
- `docs/case-studies/2026-05-web-access-analysis.md`
- `docs/case-studies/2026-05-business-opportunity-skill-scan.md`
- `skills/prior-art-scout/references/search-adapters.md`
