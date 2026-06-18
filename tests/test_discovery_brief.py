import importlib.resources
from pathlib import Path

from project_scout.core import load_brief
from project_scout.models import DiscoveryBrief


FIXTURES = Path(__file__).parent / "fixtures"
BRIEF_TEMPLATES = Path(__file__).parents[1] / "examples" / "brief-templates"


def test_load_brief_preserves_discovery_brief_fields():
    brief = load_brief(FIXTURES / "discovery_brief.json")

    assert isinstance(brief, DiscoveryBrief)
    assert brief.name == "prior-art-scout"
    assert brief.target_type == "skill"
    assert brief.intent == "build"
    assert "prior art" in brief.keywords
    assert "coverage matrix" in brief.must_have
    assert "skills registry" in brief.nice_to_have
    assert "codex users" in brief.users_or_consumers
    assert "codex skills" in brief.ecosystems
    assert "search log" in brief.must_have
    assert brief.exclusions == ["autonomous crawler"]
    assert "skills.volces.com@github-research" in brief.known_candidates


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
        if isinstance(brief, DiscoveryBrief):
            assert brief.users_or_consumers
            assert brief.ecosystems
        else:
            assert brief.target_users
            assert brief.tech_stack
        assert brief.exclusions


def test_packaged_brief_templates_match_example_templates():
    package_templates = importlib.resources.files("project_scout").joinpath("brief_templates")

    for example_path in sorted(BRIEF_TEMPLATES.glob("*.json")):
        package_path = package_templates.joinpath(example_path.name)
        assert package_path.read_text() == example_path.read_text()
