# Conductor Boundary

`project-scout` is an independent CLI/library and skill source repository. It
is not part of Conductor Core.

## Allowed Integration Shape

- Conductor may call `project-scout` as an external local tool.
- A future Conductor plugin may wrap the CLI after a separate approval and
  design pass.
- Reports should remain file-based JSON and Markdown artifacts.
- Fixture-first validation remains the default for any wrapper.

## Not In Scope

- Moving `project-scout` modules into Conductor Core.
- Making Conductor responsible for live crawling, web sessions, or tokens.
- Treating `project-scout` recommendations as automatic roadmap decisions.
- Pushing, publishing, or opening pull requests from `project-scout` runs.

## Stable Local Commands

Use the installed console script after `scripts/bootstrap-dev.sh`:

```bash
.venv/bin/project-scout report \
  --brief tests/fixtures/brief.json \
  --candidates tests/fixtures/github_repos.json \
  --out-json /tmp/project-scout-conductor-boundary.json \
  --out-md /tmp/project-scout-conductor-boundary.md
```

Use the source-tree fallback only for local recovery:

```bash
PYTHONPATH=src .venv/bin/python -m project_scout.cli report \
  --brief tests/fixtures/brief.json \
  --candidates tests/fixtures/github_repos.json \
  --out-json /tmp/project-scout-conductor-boundary-fallback.json \
  --out-md /tmp/project-scout-conductor-boundary-fallback.md
```
