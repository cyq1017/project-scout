#!/usr/bin/env sh
set -eu

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$repo_root"

find_python() {
  if [ "${PYTHON_BIN:-}" ]; then
    command -v "$PYTHON_BIN"
    return
  fi

  for candidate in python3.13 python3.12 python3.11 python3; do
    if command -v "$candidate" >/dev/null 2>&1; then
      command -v "$candidate"
      return
    fi
  done

  return 1
}

python_bin=$(find_python) || {
  echo "No Python 3 interpreter found. Install Python 3.12 or 3.13 and retry." >&2
  exit 1
}

version=$("$python_bin" - <<'PY'
import sys
print(f"{sys.version_info.major}.{sys.version_info.minor}")
PY
)

case "$version" in
  3.12|3.13)
    ;;
  3.10|3.11)
    echo "Using Python $version. Python 3.12 or 3.13 is recommended for this repo." >&2
    ;;
  3.14)
    echo "Python 3.14 can create hidden/dataless editable installs on macOS." >&2
    echo "Install Python 3.12 or 3.13, or rerun with PROJECT_SCOUT_ALLOW_PY314=1 to proceed." >&2
    if [ "${PROJECT_SCOUT_ALLOW_PY314:-}" != "1" ]; then
      exit 1
    fi
    ;;
  *)
    echo "Unsupported Python $version. Use Python 3.10 through 3.13." >&2
    exit 1
    ;;
esac

echo "Rebuilding .venv with $python_bin (Python $version)"
venv_parent=${PROJECT_SCOUT_VENV_PARENT:-${XDG_CACHE_HOME:-"$HOME/.cache"}/project-scout}
venv_dir=${PROJECT_SCOUT_VENV_DIR:-"$venv_parent/venv"}
stale_venv=${TMPDIR:-/tmp}/project-scout-stale-venv-$$

mkdir -p "$(dirname "$venv_dir")"
rm -rf "$venv_dir"

if [ -L .venv ]; then
  rm .venv
elif [ -e .venv ]; then
  mv .venv "$stale_venv"
  echo "Moved old in-repo .venv to $stale_venv"
fi

"$python_bin" -m venv "$venv_dir"
ln -s "$venv_dir" .venv
.venv/bin/python -m pip install -U pip setuptools wheel
.venv/bin/python -m pip install -e ".[dev]"

scripts/smoke.sh

echo
echo "Bootstrap complete. Next verification:"
echo ".venv/bin/python -m pytest"
