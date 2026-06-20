import json
import re
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
SECRET_PATTERNS = (
    re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"Authorization:\s*Bearer\s+[A-Za-z0-9._-]{20,}", re.IGNORECASE),
)
RAW_DUMP_FILENAME_MARKERS = ("raw", "dump", "cookie", "session", "private")
RAW_DUMP_JSON_KEYS = {
    "access_token",
    "authorization",
    "cookie",
    "cookies",
    "headers",
    "html",
    "html_body",
    "page_source",
    "private_data",
    "raw",
    "raw_dump",
    "raw_results",
    "refresh_token",
}


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


def test_public_docs_and_examples_do_not_include_secret_values():
    leaked = []
    for relative_path in _tracked_public_files():
        text = (ROOT / relative_path).read_text(encoding="utf-8")
        if any(pattern.search(text) for pattern in SECRET_PATTERNS):
            leaked.append(relative_path)

    assert leaked == []


def test_examples_are_curated_outputs_not_raw_dumps():
    bad_filenames = []
    bad_keys = []
    for path in (ROOT / "examples").rglob("*"):
        if path.is_dir():
            continue
        lower_name = path.name.lower()
        if any(marker in lower_name for marker in RAW_DUMP_FILENAME_MARKERS):
            bad_filenames.append(str(path.relative_to(ROOT)))
        if path.suffix == ".json":
            data = json.loads(path.read_text(encoding="utf-8"))
            _collect_raw_dump_keys(data, path.relative_to(ROOT), bad_keys)

    assert bad_filenames == []
    assert bad_keys == []


def test_m5_release_hardening_is_marked_complete():
    milestone = (ROOT / "docs" / "milestones" / "m5-release-hardening.md").read_text(
        encoding="utf-8"
    )
    backlog = (ROOT / "BACKLOG.md").read_text(encoding="utf-8")

    assert "Status: Complete" in milestone
    assert "- [x] M5: Release hardening." in backlog
    assert "- [x] Add public release-readiness examples without raw dumps or private artifacts." in backlog
    assert "Public examples were audited" in milestone


def _tracked_public_files() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    return [
        relative_path
        for relative_path in result.stdout.splitlines()
        if relative_path.startswith(PUBLIC_PATH_PREFIXES)
    ]


def _collect_raw_dump_keys(
    value: object,
    path: Path,
    bad_keys: list[str],
) -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            if key.lower() in RAW_DUMP_JSON_KEYS:
                bad_keys.append(f"{path}:{key}")
            _collect_raw_dump_keys(nested, path, bad_keys)
    elif isinstance(value, list):
        for item in value:
            _collect_raw_dump_keys(item, path, bad_keys)
