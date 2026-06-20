#!/usr/bin/env sh
set -eu

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$repo_root"

if [ ! -x ".venv/bin/python" ]; then
  echo "Missing .venv/bin/python. Run scripts/bootstrap-dev.sh first." >&2
  exit 1
fi

wheelhouse=$(mktemp -d "${TMPDIR:-/tmp}/project-scout-wheelhouse.XXXXXX")
venv_dir=$(mktemp -d "${TMPDIR:-/tmp}/project-scout-wheel-venv.XXXXXX")
run_dir=$(mktemp -d "${TMPDIR:-/tmp}/project-scout-wheel-run.XXXXXX")

cleanup() {
  rm -rf "$wheelhouse" "$venv_dir" "$run_dir"
}
trap cleanup EXIT INT TERM

.venv/bin/python -m pip wheel . -w "$wheelhouse"
.venv/bin/python -m venv "$venv_dir"
"$venv_dir/bin/python" -m pip install "$wheelhouse"/project_scout-*.whl

cd "$run_dir"
"$venv_dir/bin/project-scout" report \
  --brief "$repo_root/tests/fixtures/brief.json" \
  --candidates "$repo_root/tests/fixtures/github_repos.json" \
  --out-json /tmp/project-scout-wheel.json \
  --out-md /tmp/project-scout-wheel.md \
  --generated-at 2026-06-04T00:00:00+00:00
