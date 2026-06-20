import json
from pathlib import Path

from project_scout.core import build_report
from project_scout.models import CandidateRepo, DiscoveryBrief, ProjectBrief
from project_scout.report import render_markdown


ROOT = Path(__file__).resolve().parents[1]
QUALITY_CASES = ROOT / "tests" / "quality_cases"
REQUIRED_CASES = {
    "agentux_terminal_selection",
    "direct_adoption_candidate",
    "thin_coverage_hold",
}


def test_research_quality_cases_cover_core_decision_shapes():
    cases = _load_quality_cases()

    assert set(cases) >= REQUIRED_CASES

    target_types = {case["brief"].get("target_type", "project") for case in cases.values()}
    assert {"product", "project", "skill"} <= target_types


def test_research_quality_cases_match_expected_decision_contracts():
    for case_name, case in _load_quality_cases().items():
        brief = _brief_from_dict(case["brief"])
        candidates = [CandidateRepo.from_dict(item) for item in case["candidates"]]
        report = build_report(
            brief,
            candidates,
            generated_at="2026-06-21T00:00:00+08:00",
            search_log=case.get("search_log", []),
        )
        data = report.to_dict()
        expected = case["expected"]
        markdown = render_markdown(report)

        assert data["decision"]["recommendation"] == expected["decision"], case_name
        assert data["coverage"]["confidence"] == expected["coverage_confidence"], case_name
        assert data["decision_dashboard"]["go_no_go"] == expected["go_no_go"], case_name
        assert (
            data["differentiation"]["positioning_brief"]["closest_alternatives"][0]["name"]
            == expected["closest_alternative"]
        ), case_name
        for phrase in expected.get("markdown_contains", []):
            assert phrase in markdown, case_name
        for phrase in expected.get("claims_to_avoid_contains", []):
            assert any(
                phrase in item for item in data["differentiation"]["claims_to_avoid"]
            ), case_name


def test_m6_milestone_documents_quality_harness():
    milestone = (ROOT / "docs" / "milestones" / "m6-research-quality-harness.md").read_text(
        encoding="utf-8"
    )
    backlog = (ROOT / "BACKLOG.md").read_text(encoding="utf-8")

    assert "Status: In Progress" in milestone
    assert "tests/quality_cases" in milestone
    assert "agentux_terminal_selection" in milestone
    assert "direct_adoption_candidate" in milestone
    assert "thin_coverage_hold" in milestone
    assert "- [ ] M6: Research quality harness." in backlog


def _load_quality_cases() -> dict[str, dict]:
    cases = {}
    for path in sorted(QUALITY_CASES.glob("*.json")):
        case = json.loads(path.read_text(encoding="utf-8"))
        cases[case["name"]] = case
    return cases


def _brief_from_dict(data: dict) -> ProjectBrief | DiscoveryBrief:
    if "target_type" in data or "users_or_consumers" in data:
        return DiscoveryBrief.from_dict(data)
    return ProjectBrief.from_dict(data)
