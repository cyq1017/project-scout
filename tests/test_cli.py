import json
import os
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path


FIXTURES = Path(__file__).parent / "fixtures"


def test_cli_generates_fixture_report(tmp_path):
    out_json = tmp_path / "project-scout-report.json"
    out_md = tmp_path / "docs" / "research" / "2026-05-prior-art-map.md"

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "project_scout.cli",
            "report",
            "--brief",
            str(FIXTURES / "brief.json"),
            "--candidates",
            str(FIXTURES / "github_repos.json"),
            "--out-json",
            str(out_json),
            "--out-md",
            str(out_md),
            "--generated-at",
            "2026-05-24T00:00:00Z",
        ],
        check=False,
        text=True,
        capture_output=True,
        env={**os.environ, "PYTHONPATH": "src"},
    )

    assert result.returncode == 0, result.stderr
    assert "Wrote" in result.stdout
    assert json.loads(out_json.read_text())["brief"]["name"] == "project-scout"
    assert "## Executive Summary" in out_md.read_text()


def test_default_markdown_path_uses_current_year_and_month(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "project_scout.cli",
            "report",
            "--brief",
            str(FIXTURES / "brief.json"),
            "--candidates",
            str(FIXTURES / "github_repos.json"),
            "--out-json",
            str(tmp_path / "report.json"),
            "--generated-at",
            "2026-05-24T00:00:00Z",
        ],
        check=False,
        text=True,
        capture_output=True,
        cwd=tmp_path,
        env={**os.environ, "PYTHONPATH": str(Path.cwd() / "src")},
    )

    month = datetime.now(UTC).strftime("%Y-%m")
    out_md = tmp_path / "docs" / "research" / f"{month}-prior-art-map.md"
    assert result.returncode == 0, result.stderr
    assert out_md.exists()
