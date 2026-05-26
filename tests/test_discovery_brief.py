from pathlib import Path

from project_scout.core import load_brief


FIXTURES = Path(__file__).parent / "fixtures"


def test_load_brief_maps_discovery_brief_to_project_brief():
    brief = load_brief(FIXTURES / "discovery_brief.json")

    assert brief.name == "prior-art-scout"
    assert "prior art" in brief.keywords
    assert "coverage matrix" in brief.keywords
    assert "skills registry" in brief.keywords
    assert "codex users" in brief.target_users
    assert "codex skills" in brief.tech_stack
    assert "search log" in brief.tech_stack
    assert brief.exclusions == ["autonomous crawler"]


def test_load_brief_preserves_project_brief_schema():
    brief = load_brief(FIXTURES / "brief.json")

    assert brief.name == "project-scout"
    assert "github search" in brief.keywords
    assert "staff engineers" in brief.target_users
