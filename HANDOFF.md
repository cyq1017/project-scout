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

Current milestone:

- M1 local prior-art gate is documented in
  `docs/milestones/m1-local-prior-art-gate.md`.
- Treat M1 as achieved when bootstrap, pytest, smoke, wheel install smoke,
  sample reports, report schema, and skill contract all match.
- M2 should dogfood one real-world formal gate report before adding broad new
  adapters or platform behavior.

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

Trustworthiness hardening status:

- Candidate-level recommendations no longer use `Write New`.
- `Write New` is a report-level decision only when coverage is high and no
  candidate is strong enough to adopt, integrate, fork, or borrow.
- Empty candidate sets and failed live sources should still write partial
  reports with `Research More` and recorded blind spots.
- Decision confidence is heuristic and is capped by coverage confidence.
- Markdown reports escape table and list content before rendering.
- Discovery briefs remain intact in report JSON; scoring uses an internal
  normalized view rather than destructively converting the brief at load time.
- Coverage now records target-specific source requirements and known-candidate
  misses as blind spots.
- Candidates can carry `kind` and source-specific `attributes` for non-repo
  assets such as products, papers, skills, plugins, and MCP-style servers.
- Relevance matching includes basic CJK lexical overlap in addition to ASCII
  tokens.
- Scored candidates include structured `evidence_records` for license,
  maintenance, primary-source URL, integration, and pricing/security. Unknown
  adoption evidence caps decision confidence and must be resolved manually.
- Candidate disposition and report-level decision gates live in
  `project_scout.recommendation`; keep scoring deterministic and separate from
  adoption readiness.
- Reports include a deterministic `differentiation` map with similarity
  clusters, commodity features, unique combination, defensible positioning,
  claims to avoid, borrow/integrate/compete guidance, and a conservative README
  positioning draft.
- Markdown reports include a first-page `Positioning Brief` with verdict,
  closest alternatives, candidate roles, recommended positioning, and next
  validation steps.
- Reports include a first-page `Decision Dashboard` with `go`/`review`/`hold`,
  primary action, review queue, and open questions. This is a deterministic
  human-review checklist, not an automatic approval or roadmap mutation.

The larger GPT Pro architecture review is local-only unless intentionally
curated into repo docs. The current executable roadmap is
`docs/plans/2026-06-18-trustworthiness-hardening.md`.

Experience library entry points:

- `docs/patterns/skill-experience-library.md`
- `docs/patterns/search-routing-pattern.md`
- `docs/case-studies/2026-05-web-access-analysis.md`
- `docs/case-studies/2026-05-business-opportunity-skill-scan.md`
- `skills/prior-art-scout/references/search-adapters.md`
