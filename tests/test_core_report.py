import json
from pathlib import Path

from project_scout.core import build_report, load_brief, load_candidates
from project_scout.models import CandidateRepo, ProjectBrief
from project_scout.report import render_markdown, write_report


FIXTURES = Path(__file__).parent / "fixtures"


def test_build_report_ranks_candidates_and_records_overlap_evidence():
    brief = load_brief(FIXTURES / "brief.json")
    candidates = load_candidates(FIXTURES / "github_repos.json")

    report = build_report(brief, candidates, generated_at="2026-05-24T00:00:00Z")

    assert report.summary.candidate_count == 3
    assert report.candidates[0].name == "sample/prior-art-cli"
    assert report.candidates[0].similarity_score > report.candidates[1].similarity_score
    assert report.candidates[0].recommendation in {"Adopt", "Borrow", "Integrate", "Fork", "Write New"}
    assert all(candidate.recommendation != "Compete" for candidate in report.candidates)
    assert "python" in report.candidates[0].evidence
    assert all("and" not in candidate.evidence for candidate in report.candidates)
    assert "analysi" not in report.candidates[0].evidence
    assert "github search" not in report.candidates[1].evidence
    assert report.overlap_matrix[0]["candidate"] == "sample/prior-art-cli"
    assert report.overlap_matrix[0]["keyword_overlap"] >= 3


def test_build_report_includes_decision_coverage_and_search_log():
    brief = load_brief(FIXTURES / "brief.json")
    candidates = load_candidates(FIXTURES / "github_repos.json")

    report = build_report(
        brief,
        candidates,
        generated_at="2026-05-24T00:00:00Z",
        search_log=[
            {
                "source": "manual",
                "query": "tests/fixtures/github_repos.json",
                "result_count": 3,
                "used_count": 3,
                "status": "ok",
                "error": None,
            }
        ],
    )
    data = report.to_dict()

    assert data["decision"]["recommendation"] == report.candidates[0].recommendation
    assert data["decision"]["confidence"] in {"Low", "Medium", "High"}
    assert data["coverage"]["confidence"] == "Medium"
    assert data["coverage"]["sources"][0]["source"] == "manual"
    assert data["coverage"]["blind_spots"]
    assert data["search_log"][0]["used_count"] == 3


def test_failed_search_source_is_recorded_as_blind_spot():
    brief = load_brief(FIXTURES / "brief.json")
    candidates = load_candidates(FIXTURES / "github_repos.json")

    report = build_report(
        brief,
        candidates,
        generated_at="2026-05-24T00:00:00Z",
        search_log=[
            {
                "source": "skills",
                "query": "prior art skill",
                "result_count": 0,
                "used_count": 0,
                "status": "failed",
                "error": "registry unavailable",
            },
            {
                "source": "web",
                "query": "prior art tool",
                "result_count": 2,
                "used_count": 1,
                "status": "ok",
                "error": None,
            },
        ],
    )

    assert report.coverage.confidence == "Low"
    assert any("skills source failed" in item for item in report.coverage.blind_spots)
    assert all("No major source-class blind spots" not in item for item in report.coverage.blind_spots)


def test_write_new_suggested_update_explains_no_candidate_is_sufficient():
    brief = ProjectBrief(
        name="business-opportunity-discovery-skill",
        goal="Find business opportunity discovery tools before building.",
        keywords=["business opportunity discovery", "market research", "startup idea validation"],
        target_users=["founders"],
        tech_stack=["skill", "web search"],
        exclusions=[],
    )
    candidates = [
        CandidateRepo(
            name="startup-idea-validation",
            url="https://example.com/startup-idea-validation",
            description="Startup idea validation and market research workflow.",
            topics=["market-research"],
            license="",
            language="Markdown",
        )
    ]

    report = build_report(brief, candidates, generated_at="2026-05-24T00:00:00Z")

    assert report.candidates[0].recommendation == "Write New"
    assert "no candidate is sufficient" in report.suggested_updates[0]


def test_render_markdown_contains_required_sections_and_recommendation():
    brief = load_brief(FIXTURES / "brief.json")
    candidates = load_candidates(FIXTURES / "github_repos.json")
    report = build_report(brief, candidates, generated_at="2026-05-24T00:00:00Z")

    markdown = render_markdown(report)

    for heading in [
        "Executive Summary",
        "Search Summary",
        "Coverage Matrix",
        "Similar Projects",
        "Overlap Matrix",
        "What To Borrow",
        "What To Avoid",
        "Recommendation And Confidence",
        "Coverage Confidence And Blind Spots",
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
