#!/usr/bin/env sh
set -eu

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$repo_root"

if [ ! -x ".venv/bin/python" ]; then
  echo "Missing .venv/bin/python. Run scripts/bootstrap-dev.sh first." >&2
  exit 1
fi

if [ ! -x ".venv/bin/project-scout" ]; then
  echo "Missing .venv/bin/project-scout. Run scripts/bootstrap-dev.sh first." >&2
  exit 1
fi

.venv/bin/project-scout report \
  --brief tests/fixtures/brief.json \
  --candidates tests/fixtures/github_repos.json \
  --out-json /tmp/project-scout-entrypoint.json \
  --out-md /tmp/project-scout-entrypoint.md \
  --generated-at 2026-06-04T00:00:00+00:00

PYTHONPATH=src .venv/bin/python -m project_scout.cli report \
  --brief tests/fixtures/brief.json \
  --candidates tests/fixtures/github_repos.json \
  --out-json /tmp/project-scout-smoke.json \
  --out-md /tmp/project-scout-smoke.md \
  --generated-at 2026-06-04T00:00:00+00:00
