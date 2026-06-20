import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check-agentux-dogfood-artifacts.py"


def _write_complete_bundle(path: Path) -> None:
    (path / "agentux-brief.json").write_text(
        json.dumps(
            {
                "name": "AgentUX",
                "target_type": "product",
                "goal": "Research selection-aware terminal UX for CLI coding agents.",
            }
        ),
        encoding="utf-8",
    )
    (path / "agentux-candidates.json").write_text(
        json.dumps(
            [
                {
                    "name": "Send to iTerm2 Claude Code",
                    "url": "https://example.com/send-to-iterm2-claude-code",
                    "kind": "ide_extension",
                }
            ]
        ),
        encoding="utf-8",
    )
    (path / "agentux-report.json").write_text(
        json.dumps(
            {
                "summary": {"candidate_count": 1, "top_recommendation": "Write New"},
                "decision": {"recommendation": "Write New", "confidence": "Medium"},
                "decision_dashboard": {
                    "status": "ready_for_manual_review",
                    "go_no_go": "review",
                    "primary_action": "Review closest adjacent candidates.",
                },
                "coverage": {
                    "confidence": "High",
                    "blind_spots": ["Skills registry not searched."],
                    "source_requirements": [
                        {"source": "manual", "required": True, "status": "covered"},
                        {"source": "web", "required": True, "status": "covered"},
                    ],
                },
                "differentiation": {
                    "claims_to_avoid": ["Do not claim exhaustive discovery."],
                    "borrow_integrate_compete_guidance": [
                        "Borrow editor-selection handoff patterns."
                    ],
                },
                "search_log": [
                    {
                        "source": "web",
                        "query": "iTerm2 selection AI",
                        "result_count": 3,
                        "used_count": 1,
                        "status": "ok",
                    }
                ],
                "candidates": [{"name": "Send to iTerm2 Claude Code"}],
            }
        ),
        encoding="utf-8",
    )
    (path / "agentux-prior-art-map.md").write_text(
        "# AgentUX Prior Art\n\n## Decision Dashboard\n\n## Coverage Confidence And Blind Spots\n",
        encoding="utf-8",
    )
    (path / "agentux-source-log.md").write_text(
        "# Source Log\n\n## Query Matrix Applied\n\n| Family | Queries |\n| --- | --- |\n",
        encoding="utf-8",
    )
    (path / "agentux-chat-summary.md").write_text(
        "# Summary\n\nDirect competitor: none found.\nCoverage confidence: High.\nClaims to avoid: exhaustive search.\nNext validation step: primary-source review.\n",
        encoding="utf-8",
    )


def test_agentux_artifact_checker_accepts_complete_bundle(tmp_path):
    _write_complete_bundle(tmp_path)

    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--dir", str(tmp_path)],
        check=False,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stderr
    assert "PASS" in result.stdout
    assert "agentux-report.json" in result.stdout


def test_agentux_artifact_checker_rejects_missing_source_log(tmp_path):
    _write_complete_bundle(tmp_path)
    (tmp_path / "agentux-source-log.md").unlink()

    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--dir", str(tmp_path)],
        check=False,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 1
    assert "agentux-source-log.md" in result.stdout


def test_agentux_artifact_checker_accepts_should_not_claim_guardrail(tmp_path):
    _write_complete_bundle(tmp_path)
    (tmp_path / "agentux-chat-summary.md").write_text(
        "# Summary\n\nDirect competitor: none found.\nCoverage confidence: High.\n"
        "AgentUX should not claim uniqueness around terminal selection alone.\n"
        "Next validation step: primary-source review.\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--dir", str(tmp_path)],
        check=False,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 0, result.stdout


def test_agentux_artifact_checker_reports_invalid_candidate_count(tmp_path):
    _write_complete_bundle(tmp_path)
    report_path = tmp_path / "agentux-report.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    report["summary"]["candidate_count"] = "many"
    report_path.write_text(json.dumps(report), encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--dir", str(tmp_path)],
        check=False,
        text=True,
        capture_output=True,
    )

    assert result.returncode == 1
    assert "candidate_count" in result.stdout
    assert "Traceback" not in result.stderr


def test_agentux_artifact_checker_is_documented_for_forward_test_review():
    required_docs = [
        ROOT / "docs" / "plans" / "2026-06-20-agentux-dogfood-prompt.md",
        ROOT / "docs" / "milestones" / "m2-skill-quality-gate.md",
        ROOT / "HANDOFF.md",
    ]

    for path in required_docs:
        assert path.exists()
        assert "check-agentux-dogfood-artifacts.py" in path.read_text(encoding="utf-8")
