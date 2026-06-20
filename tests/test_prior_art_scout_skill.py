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


def test_agentux_dogfood_case_study_records_source_profile_lesson():
    case_study = DOCS / "case-studies" / "2026-06-agentux-skill-quality-dogfood.md"
    source_routing = REFERENCES / "source-routing.md"

    assert case_study.exists()

    case_text = case_study.read_text(encoding="utf-8")
    routing_text = source_routing.read_text(encoding="utf-8")

    assert "AgentUX" in case_text
    assert "curated web candidates" in case_text
    assert "manual known-candidate file" in case_text
    assert "curated web candidates" in routing_text
    assert "manual known-candidate file" in routing_text


def test_prior_art_scout_links_m4_due_diligence_references():
    skill = SKILL_MD.read_text(encoding="utf-8")

    for reference in [
        "references/due-diligence-gate.md",
        "references/candidate-evidence.md",
        "references/anti-rationalizations.md",
        "references/skill-pack-routing.md",
    ]:
        assert reference in skill
        assert (SKILL_DIR / reference).exists()

    for section in [
        "## Core Process",
        "## Red Flags",
        "## Verification",
        "## Exit Criteria",
    ]:
        assert section in skill

    assert "project-scout` CLI/library" in skill
    assert "deterministic" in skill


def test_prior_art_scout_m4_references_define_due_diligence_boundaries():
    for filename in [
        "due-diligence-gate.md",
        "candidate-evidence.md",
        "anti-rationalizations.md",
        "skill-pack-routing.md",
    ]:
        reference = REFERENCES / filename
        assert reference.exists()
        text = reference.read_text(encoding="utf-8").lower()
        assert "project-scout" in text
        assert "automatic final decision" not in text
        assert "legal due diligence" not in text
        assert "financial due diligence" not in text

    due_diligence = (REFERENCES / "due-diligence-gate.md").read_text(encoding="utf-8")
    assert "No exhaustive-search claim is made" in due_diligence
    assert "Formal Gate" in due_diligence
    assert "Quick Scan" in due_diligence


def test_prior_art_scout_blocks_false_confidence_rationalizations():
    text = (REFERENCES / "anti-rationalizations.md").read_text(encoding="utf-8").lower()

    for shortcut in [
        "no results means no competitors",
        "stars prove adoption",
        "llm summary replaces primary source",
        "coverage low but recommendation high",
        "write new from one weak candidate",
        "failed adapter can be ignored",
    ]:
        assert shortcut in text
