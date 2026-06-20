import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_PATH_PREFIXES = (
    "BACKLOG.md",
    "DEVLOG.md",
    "HANDOFF.md",
    "README.md",
    "docs/",
    "examples/",
    "skills/",
)
LOCAL_PATH_MARKERS = (
    "/Users/caoyuqi",
    "/Volumes/",
)


def test_public_docs_and_examples_do_not_include_local_absolute_paths():
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )

    leaked = []
    for relative_path in result.stdout.splitlines():
        if not relative_path.startswith(PUBLIC_PATH_PREFIXES):
            continue
        path = ROOT / relative_path
        text = path.read_text(encoding="utf-8")
        if any(marker in text for marker in LOCAL_PATH_MARKERS):
            leaked.append(relative_path)

    assert leaked == []
