import importlib.resources
from pathlib import Path

from project_scout.core import load_brief


FIXTURES = Path(__file__).parent / "fixtures"
BRIEF_TEMPLATES = Path(__file__).parents[1] / "examples" / "brief-templates"


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


def test_example_brief_templates_load_as_project_briefs():
    template_paths = sorted(BRIEF_TEMPLATES.glob("*.json"))

    assert {path.name for path in template_paths} == {
        "agent-plugin.json",
        "cli-library.json",
        "skill-discovery.json",
    }
    for path in template_paths:
        brief = load_brief(path)
        assert brief.name.startswith("replace-with-")
        assert brief.goal
        assert brief.keywords
        assert brief.target_users
        assert brief.tech_stack
        assert brief.exclusions


def test_packaged_brief_templates_match_example_templates():
    package_templates = importlib.resources.files("project_scout").joinpath("brief_templates")

    for example_path in sorted(BRIEF_TEMPLATES.glob("*.json")):
        package_path = package_templates.joinpath(example_path.name)
        assert package_path.read_text() == example_path.read_text()
