#!/usr/bin/env sh
set -eu

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$repo_root"

skill_home=${PROJECT_SCOUT_SKILL_HOME:-"$HOME/.codex/skills"}
skill_name=prior-art-scout
source_dir="skills/$skill_name"
target_dir="$skill_home/$skill_name"

if [ ! -f "$source_dir/SKILL.md" ]; then
  echo "Missing skill source at $source_dir" >&2
  exit 1
fi

mkdir -p "$skill_home"
rm -rf "$target_dir"
cp -R "$source_dir" "$target_dir"

echo "Installed $skill_name to $target_dir"
