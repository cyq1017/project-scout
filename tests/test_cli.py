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

    data = json.loads(out_json.read_text())
    assert data["search_log"][0]["source"] == "manual"
    assert data["coverage"]["sources"][0]["status"] == "ok"
    assert data["decision"]["confidence"] in {"Low", "Medium", "High"}


def test_console_script_generates_fixture_report_without_pythonpath(tmp_path):
    console_script = Path(sys.executable).with_name("project-scout")
    assert console_script.exists(), (
        f"Missing console script at {console_script}. "
        "Run scripts/bootstrap-dev.sh before using the pytest gate."
    )

    out_json = tmp_path / "entrypoint-report.json"
    out_md = tmp_path / "entrypoint-report.md"
    env = {**os.environ}
    env.pop("PYTHONPATH", None)

    result = subprocess.run(
        [
            str(console_script),
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
            "2026-06-04T00:00:00+00:00",
        ],
        check=False,
        text=True,
        capture_output=True,
        env=env,
    )

    assert result.returncode == 0, result.stderr
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


def test_cli_records_skills_registry_candidates(tmp_path, monkeypatch):
    from project_scout import cli
    from project_scout.models import CandidateRepo

    def fake_search(query, *, timeout=None):
        assert query == "prior art skill"
        assert timeout == 30
        return [
            CandidateRepo(
                name="skills.volces.com@github-research",
                url="https://skills.sh/skills.volces.com/github-research",
                description="Skill registry result.",
                topics=["skill", "skills-registry"],
            )
        ]

    monkeypatch.setattr(cli, "search_skills_registry", fake_search)
    out_json = tmp_path / "report.json"
    out_md = tmp_path / "report.md"

    result = cli.main(
        [
            "report",
            "--brief",
            str(FIXTURES / "discovery_brief.json"),
            "--candidates",
            str(FIXTURES / "github_repos.json"),
            "--skills-query",
            "prior art skill",
            "--out-json",
            str(out_json),
            "--out-md",
            str(out_md),
            "--generated-at",
            "2026-05-24T00:00:00Z",
        ]
    )

    data = json.loads(out_json.read_text())
    assert result == 0
    assert any(entry["source"] == "skills" for entry in data["search_log"])
    assert any(candidate["name"] == "skills.volces.com@github-research" for candidate in data["candidates"])


def test_cli_records_web_candidates_and_summary_overrides(tmp_path):
    from project_scout import cli

    out_json = tmp_path / "report.json"
    out_md = tmp_path / "report.md"

    result = cli.main(
        [
            "report",
            "--brief",
            str(FIXTURES / "brief.json"),
            "--web-candidates",
            str(FIXTURES / "web_candidates.json"),
            "--summary-overrides",
            str(FIXTURES / "summary_overrides.json"),
            "--out-json",
            str(out_json),
            "--out-md",
            str(out_md),
            "--generated-at",
            "2026-06-04T00:00:00+00:00",
        ]
    )

    data = json.loads(out_json.read_text())
    assert result == 0
    assert data["candidates"][0]["readme_summary"] == "LLM-prepared summary from an external offline review."
    assert any(entry["source"] == "web" for entry in data["search_log"])
    assert any(entry["source"] == "summary_overrides" for entry in data["search_log"])


def test_cli_accepts_score_weights_file(tmp_path):
    from project_scout import cli

    out_json = tmp_path / "report.json"
    out_md = tmp_path / "report.md"

    result = cli.main(
        [
            "report",
            "--brief",
            str(FIXTURES / "brief.json"),
            "--candidates",
            str(FIXTURES / "github_repos.json"),
            "--weights",
            str(FIXTURES / "score_weights_stack.json"),
            "--out-json",
            str(out_json),
            "--out-md",
            str(out_md),
            "--generated-at",
            "2026-06-04T00:00:00+00:00",
        ]
    )

    assert result == 0
    assert json.loads(out_json.read_text())["summary"]["candidate_count"] == 3


def test_cli_merges_multiple_github_queries_by_url(tmp_path, monkeypatch):
    from project_scout import cli
    from project_scout.models import CandidateRepo

    calls = []

    def fake_search(query, *, limit, timeout=None, include_readme=True):
        calls.append((query, limit))
        assert timeout == 20
        assert include_readme is True
        return [
            CandidateRepo(
                name=f"{query}-shared",
                url="https://github.com/example/shared",
                description=f"Shared result for {query}.",
            ),
            CandidateRepo(
                name=f"{query}-unique",
                url=f"https://github.com/example/{query.replace(' ', '-')}",
                description=f"Unique result for {query}.",
            ),
        ]

    monkeypatch.setattr(cli, "search_github_repositories", fake_search)
    out_json = tmp_path / "report.json"
    out_md = tmp_path / "report.md"

    result = cli.main(
        [
            "report",
            "--brief",
            str(FIXTURES / "brief.json"),
            "--github-query",
            "prior art cli",
            "--github-query",
            "project discovery",
            "--github-limit",
            "3",
            "--out-json",
            str(out_json),
            "--out-md",
            str(out_md),
            "--generated-at",
            "2026-06-04T00:00:00+00:00",
        ]
    )

    data = json.loads(out_json.read_text())
    urls = [candidate["url"] for candidate in data["candidates"]]
    github_entries = [entry for entry in data["search_log"] if entry["source"] == "github"]
    assert result == 0
    assert calls == [("prior art cli", 3), ("project discovery", 3)]
    assert urls.count("https://github.com/example/shared") == 1
    assert len(github_entries) == 2
    assert {entry["query"] for entry in github_entries} == {"prior art cli", "project discovery"}


def test_cli_passes_github_timeout_and_readme_policy(tmp_path, monkeypatch):
    from project_scout import cli
    from project_scout.models import CandidateRepo

    calls = []

    def fake_search(query, *, limit, timeout=None, include_readme=True):
        calls.append((query, limit, timeout, include_readme))
        return [
            CandidateRepo(
                name="example/live",
                url="https://github.com/example/live",
                description="Live source candidate.",
            )
        ]

    monkeypatch.setattr(cli, "search_github_repositories", fake_search)
    out_json = tmp_path / "report.json"
    out_md = tmp_path / "report.md"

    result = cli.main(
        [
            "report",
            "--brief",
            str(FIXTURES / "brief.json"),
            "--github-query",
            "prior art cli",
            "--github-limit",
            "3",
            "--github-timeout",
            "4",
            "--no-github-readme",
            "--out-json",
            str(out_json),
            "--out-md",
            str(out_md),
            "--generated-at",
            "2026-06-04T00:00:00+00:00",
        ]
    )

    assert result == 0
    assert calls == [("prior art cli", 3, 4, False)]


def test_cli_records_empty_github_search_as_empty_source(tmp_path, monkeypatch):
    from project_scout import cli

    def fake_search(query, *, limit, timeout=None, include_readme=True):
        return []

    monkeypatch.setattr(cli, "search_github_repositories", fake_search)
    out_json = tmp_path / "report.json"
    out_md = tmp_path / "report.md"

    result = cli.main(
        [
            "report",
            "--brief",
            str(FIXTURES / "brief.json"),
            "--github-query",
            "prior art cli",
            "--out-json",
            str(out_json),
            "--out-md",
            str(out_md),
            "--generated-at",
            "2026-06-04T00:00:00+00:00",
        ]
    )

    data = json.loads(out_json.read_text())
    assert result == 0
    assert data["search_log"][0]["status"] == "empty"
    assert data["search_log"][0]["result_count"] == 0


def test_cli_records_github_failure_and_writes_partial_report(tmp_path, monkeypatch):
    from project_scout import cli

    def fake_search(query, *, limit, timeout=None, include_readme=True):
        raise ValueError(f"boom: {query}:{limit}:{timeout}:{include_readme}")

    monkeypatch.setattr(cli, "search_github_repositories", fake_search)
    out_json = tmp_path / "report.json"
    out_md = tmp_path / "report.md"

    result = cli.main(
        [
            "report",
            "--brief",
            str(FIXTURES / "brief.json"),
            "--github-query",
            "prior art cli",
            "--github-limit",
            "2",
            "--github-timeout",
            "3",
            "--out-json",
            str(out_json),
            "--out-md",
            str(out_md),
            "--generated-at",
            "2026-06-04T00:00:00+00:00",
        ]
    )

    data = json.loads(out_json.read_text())
    assert result == 0
    assert data["summary"]["candidate_count"] == 0
    assert data["decision"]["recommendation"] == "Research More"
    assert data["coverage"]["confidence"] == "Low"
    assert data["search_log"][0]["source"] == "github"
    assert data["search_log"][0]["status"] == "failed"
    assert "boom: prior art cli:2:3:True" in data["search_log"][0]["error"]


def test_cli_passes_skills_timeout_and_records_failure(tmp_path, monkeypatch):
    from project_scout import cli

    calls = []

    def fake_search(query, *, timeout=None):
        calls.append((query, timeout))
        raise RuntimeError("skills registry unavailable")

    monkeypatch.setattr(cli, "search_skills_registry", fake_search)
    out_json = tmp_path / "report.json"
    out_md = tmp_path / "report.md"

    result = cli.main(
        [
            "report",
            "--brief",
            str(FIXTURES / "discovery_brief.json"),
            "--skills-query",
            "prior art skill",
            "--skills-timeout",
            "5",
            "--out-json",
            str(out_json),
            "--out-md",
            str(out_md),
            "--generated-at",
            "2026-06-04T00:00:00+00:00",
        ]
    )

    data = json.loads(out_json.read_text())
    assert result == 0
    assert calls == [("prior art skill", 5)]
    assert data["search_log"][0]["source"] == "skills"
    assert data["search_log"][0]["status"] == "failed"
    assert data["search_log"][0]["error"] == "skills registry unavailable"


def test_cli_writes_partial_report_without_candidates(tmp_path):
    from project_scout import cli

    out_json = tmp_path / "report.json"
    out_md = tmp_path / "report.md"

    result = cli.main(
        [
            "report",
            "--brief",
            str(FIXTURES / "brief.json"),
            "--out-json",
            str(out_json),
            "--out-md",
            str(out_md),
            "--generated-at",
            "2026-06-04T00:00:00+00:00",
        ]
    )

    data = json.loads(out_json.read_text())
    assert result == 0
    assert data["summary"]["candidate_count"] == 0
    assert data["decision"]["recommendation"] == "Research More"
    assert "Recommendation: **Research More**" in out_md.read_text()


def test_init_brief_copies_template_without_overwrite(tmp_path):
    from project_scout import cli

    out_path = tmp_path / "skill-brief.json"

    result = cli.main(["init-brief", "--template", "skill", "--out", str(out_path)])

    data = json.loads(out_path.read_text())
    assert result == 0
    assert data["target_type"] == "skill"
    assert data["name"] == "replace-with-skill-name"

    try:
        cli.main(["init-brief", "--template", "skill", "--out", str(out_path)])
    except SystemExit as exc:
        assert "already exists" in str(exc)
    else:
        raise AssertionError("init-brief should not overwrite without --force")


def test_init_brief_force_overwrites_existing_file(tmp_path):
    from project_scout import cli

    out_path = tmp_path / "plugin-brief.json"
    out_path.write_text("{}")

    result = cli.main(
        ["init-brief", "--template", "plugin", "--out", str(out_path), "--force"]
    )

    data = json.loads(out_path.read_text())
    assert result == 0
    assert data["target_type"] == "plugin"
