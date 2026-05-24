import json
from pathlib import Path

from project_scout.core import build_report, load_brief, load_candidates
from project_scout.report import render_markdown, write_report


FIXTURES = Path(__file__).parent / "fixtures"


def test_build_report_ranks_candidates_and_records_overlap_evidence():
    brief = load_brief(FIXTURES / "brief.json")
    candidates = load_candidates(FIXTURES / "github_repos.json")

    report = build_report(brief, candidates, generated_at="2026-05-24T00:00:00Z")

    assert report.summary.candidate_count == 3
    assert report.candidates[0].name == "sample/prior-art-cli"
    assert report.candidates[0].similarity_score > report.candidates[1].similarity_score
    assert report.candidates[0].recommendation in {"Borrow", "Integrate", "Fork", "Compete"}
    assert "python" in report.candidates[0].evidence
    assert all("and" not in candidate.evidence for candidate in report.candidates)
    assert report.overlap_matrix[0]["candidate"] == "sample/prior-art-cli"
    assert report.overlap_matrix[0]["keyword_overlap"] >= 3


def test_render_markdown_contains_required_sections_and_recommendation():
    brief = load_brief(FIXTURES / "brief.json")
    candidates = load_candidates(FIXTURES / "github_repos.json")
    report = build_report(brief, candidates, generated_at="2026-05-24T00:00:00Z")

    markdown = render_markdown(report)

    for heading in [
        "Executive Summary",
        "Similar Projects",
        "Overlap Matrix",
        "What To Borrow",
        "What To Avoid",
        "Build / Adopt / Fork / Plugin Recommendation",
        "Differentiation Is Not Enough: Useful Positioning",
        "Risks And Unknowns",
        "Suggested ADR / Backlog Updates",
    ]:
        assert f"## {heading}" in markdown
    assert "sample/prior-art-cli" in markdown
    assert "Recommendation" in markdown


def test_write_report_outputs_json_and_markdown(tmp_path):
    brief = load_brief(FIXTURES / "brief.json")
    candidates = load_candidates(FIXTURES / "github_repos.json")
    report = build_report(brief, candidates, generated_at="2026-05-24T00:00:00Z")
    out_json = tmp_path / "project-scout-report.json"
    out_md = tmp_path / "docs" / "research" / "2026-05-prior-art-map.md"

    write_report(report, out_json=out_json, out_md=out_md)

    data = json.loads(out_json.read_text())
    markdown = out_md.read_text()
    assert data["summary"]["candidate_count"] == 3
    assert data["candidates"][0]["name"] == "sample/prior-art-cli"
    assert "## Similar Projects" in markdown
