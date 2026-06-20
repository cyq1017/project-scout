from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "prior-art-scout"
SKILL_MD = SKILL_DIR / "SKILL.md"
REFERENCES = SKILL_DIR / "references"
DOCS = ROOT / "docs"


def test_prior_art_scout_links_m2_quality_references():
    skill = SKILL_MD.read_text(encoding="utf-8")

    for reference in [
        "references/query-matrix.md",
        "references/positioning-discussion.md",
        "references/cross-agent-protocol.md",
    ]:
        assert reference in skill


def test_prior_art_scout_m2_references_exist_and_keep_engine_boundary():
    skill = SKILL_MD.read_text(encoding="utf-8")
    assert "project-scout` CLI/library" in skill
    assert "deterministic scoring and report generation" in skill

    for filename in [
        "query-matrix.md",
        "positioning-discussion.md",
        "cross-agent-protocol.md",
    ]:
        reference = REFERENCES / filename
        assert reference.exists()
        text = reference.read_text(encoding="utf-8").lower()
        assert "project-scout" in text
        assert "exhaustive search" not in text
        assert "automatic final decision" not in text


def test_m2_dogfood_prompt_and_milestone_define_acceptance():
    prompt = DOCS / "plans" / "2026-06-20-agentux-dogfood-prompt.md"
    milestone = DOCS / "milestones" / "m2-skill-quality-gate.md"

    assert prompt.exists()
    assert milestone.exists()

    prompt_text = prompt.read_text(encoding="utf-8")
    milestone_text = milestone.read_text(encoding="utf-8")

    assert "AgentUX" in prompt_text
    assert "/tmp" in prompt_text
    assert "Do not include expected findings" in prompt_text
    assert "source log" in milestone_text
    assert "query matrix" in milestone_text
    assert "project-scout" in milestone_text
