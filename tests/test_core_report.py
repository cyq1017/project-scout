import json
from pathlib import Path

from project_scout.core import build_report, load_brief, load_candidates
from project_scout.models import CandidateRepo, DiscoveryBrief, ProjectBrief
from project_scout.report import render_markdown, write_report


FIXTURES = Path(__file__).parent / "fixtures"


def test_build_report_ranks_candidates_and_records_overlap_evidence():
    brief = load_brief(FIXTURES / "brief.json")
    candidates = load_candidates(FIXTURES / "github_repos.json")

    report = build_report(brief, candidates, generated_at="2026-05-24T00:00:00Z")

    assert report.summary.candidate_count == 3
    assert report.candidates[0].name == "sample/prior-art-cli"
    assert report.candidates[0].similarity_score > report.candidates[1].similarity_score
    assert report.candidates[0].recommendation in {"Adopt", "Borrow", "Integrate", "Fork"}
    assert all(candidate.recommendation != "Compete" for candidate in report.candidates)
    assert "python" in report.candidates[0].evidence
    assert all("and" not in candidate.evidence for candidate in report.candidates)
    assert "analysi" not in report.candidates[0].evidence
    assert "github search" not in report.candidates[1].evidence
    assert report.overlap_matrix[0]["candidate"] == "sample/prior-art-cli"
    assert report.overlap_matrix[0]["keyword_overlap"] >= 3


def test_build_report_accepts_configurable_score_weights():
    brief = ProjectBrief(
        name="weighted-review",
        goal="Choose between keyword and stack overlap.",
        keywords=["alpha"],
        target_users=[],
        tech_stack=["python"],
        exclusions=[],
    )
    candidates = [
        CandidateRepo(
            name="keyword-match",
            url="https://example.com/keyword-match",
            description="alpha workflow",
            language="Go",
            license="MIT",
        ),
        CandidateRepo(
            name="stack-match",
            url="https://example.com/stack-match",
            description="developer tool",
            language="Python",
            license="MIT",
        ),
    ]

    report = build_report(
        brief,
        candidates,
        generated_at="2026-06-04T00:00:00+00:00",
        score_weights={
            "keyword": 0,
            "stack": 1,
            "user": 0,
            "topic": 0,
            "text": 0,
            "language_bonus": 0,
            "exclusion_multiplier": 0.75,
        },
    )

    assert report.candidates[0].name == "stack-match"


def test_build_report_scores_cjk_text_overlap():
    brief = ProjectBrief(
        name="商机发现助手",
        goal="评估是否要构建商机发现和市场研究助手。",
        keywords=["商机发现", "市场研究"],
        target_users=["创业者"],
        tech_stack=["技能"],
        exclusions=[],
    )
    candidates = [
        CandidateRepo(
            name="通用信息整理",
            url="https://example.com/generic",
            kind="product",
            description="面向团队的资料收集工具。",
        ),
        CandidateRepo(
            name="商机发现研究助手",
            url="https://example.com/opportunity",
            kind="skill",
            description="帮助创业者进行商机发现、市场研究和竞品分析。",
            topics=["商机发现", "市场研究"],
            language="Markdown",
        ),
    ]

    report = build_report(
        brief,
        candidates,
        generated_at="2026-06-04T00:00:00+00:00",
    )

    assert report.candidates[0].name == "商机发现研究助手"
    assert report.candidates[0].similarity_score > report.candidates[1].similarity_score
    assert "商机发现" in report.candidates[0].evidence


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
    assert data["coverage"]["source_requirements"]
    assert data["candidates"][0]["evidence_records"]
    assert data["differentiation"]["readme_positioning_draft"]


def test_build_report_adds_differentiation_map():
    brief = DiscoveryBrief(
        name="AgentUX",
        target_type="product",
        intent="build",
        goal=(
            "Build a selection-aware terminal UX layer for existing CLI coding agents. "
            "Users select terminal output and add it to Claude Code or Codex CLI."
        ),
        keywords=["terminal selection", "Claude Code", "Codex CLI", "branch conversation"],
        users_or_consumers=["CLI coding agent users"],
        ecosystems=["iTerm2", "terminal"],
        must_have=[
            "capture terminal output selection",
            "inject into existing CLI coding agent session",
            "branch discussion",
        ],
        nice_to_have=["iTerm2 Python API"],
        exclusions=["generic AI terminal only"],
        known_candidates=[],
    )
    candidates = [
        CandidateRepo(
            name="VS Code terminalSelection",
            url="https://example.com/vscode-terminal-selection",
            kind="ide_feature",
            description="Adds selected terminal text to an AI chat context.",
            topics=["terminal selection", "AI chat", "context"],
            attributes={"layer": "B Close adjacent"},
        ),
        CandidateRepo(
            name="Warp AI",
            url="https://example.com/warp-ai",
            kind="product",
            description="AI terminal that explains command output.",
            topics=["AI terminal", "terminal output"],
            attributes={"layer": "C Broad adjacent"},
        ),
    ]

    report = build_report(
        brief,
        candidates,
        generated_at="2026-06-20T00:00:00+08:00",
    )
    data = report.to_dict()
    differentiation = data["differentiation"]
    brief_summary = differentiation["positioning_brief"]

    assert brief_summary["verdict"] == "No direct match recorded"
    assert brief_summary["closest_alternatives"][0]["name"] == "VS Code terminalSelection"
    assert "capture terminal output selection" in brief_summary["differentiation_claim"]
    assert any("source coverage" in item for item in brief_summary["next_validation_steps"])
    assert "terminal selection" in differentiation["commodity_features"]
    assert any("capture terminal output selection" in item for item in differentiation["unique_combination"])
    assert any("combination claim" in item for item in differentiation["defensible_positioning"])
    assert any("generic AI terminal only" in item for item in differentiation["claims_to_avoid"])
    assert any("VS Code terminalSelection" in item for item in differentiation["borrow_integrate_compete_guidance"])
    assert {"candidate": "VS Code terminalSelection", "role": "integration target"} in [
        {"candidate": item["candidate"], "role": item["role"]}
        for item in differentiation["candidate_roles"]
    ]
    assert differentiation["similarity_clusters"][0]["label"] == "B Close adjacent"
    assert "existing CLI coding agents" in differentiation["readme_positioning_draft"]


def test_positioning_anchors_prioritize_explicit_close_prior_art_over_lexical_score():
    brief = DiscoveryBrief(
        name="AgentUX",
        target_type="product",
        intent="build",
        goal=(
            "Build a selection-aware terminal UX layer for existing CLI coding agents. "
            "Users select terminal output and add it to Claude Code or Codex CLI."
        ),
        keywords=[
            "terminal selection",
            "Claude Code",
            "Codex CLI",
            "branch conversation",
        ],
        users_or_consumers=["CLI coding agent users"],
        ecosystems=["iTerm2", "terminal"],
        must_have=[
            "capture terminal output selection",
            "inject into existing CLI coding agent session",
            "branch discussion",
        ],
        nice_to_have=[],
        exclusions=["generic AI terminal only"],
        known_candidates=[],
    )
    candidates = [
        CandidateRepo(
            name="Broad lexical bridge",
            url="https://example.com/broad-lexical-bridge",
            kind="tmux_bridge",
            description=(
                "Claude Code Codex CLI branch conversation terminal bridge for "
                "CLI coding agent users."
            ),
            topics=["claude-code", "codex-cli", "terminal"],
            attributes={"layer": "C Broad adjacent"},
        ),
        CandidateRepo(
            name="iTerm2 selected output Add to Chat",
            url="https://example.com/iterm2-selected-output-add-to-chat",
            kind="terminal_feature",
            description="Selected terminal output can be added to an AI chat from iTerm2.",
            topics=["terminal selection", "AI chat"],
            attributes={"layer": "A Strongest close adjacent"},
        ),
    ]

    report = build_report(
        brief,
        candidates,
        generated_at="2026-06-20T00:00:00+08:00",
    )
    positioning = report.to_dict()["differentiation"]["positioning_brief"]
    markdown = render_markdown(report)

    assert report.candidates[0].name == "Broad lexical bridge"
    assert positioning["closest_alternatives"][0]["name"] == "iTerm2 selected output Add to Chat"
    assert any(
        step == "Manually compare the workflow against iTerm2 selected output Add to Chat."
        for step in positioning["next_validation_steps"]
    )
    assert "Use iTerm2 selected output Add to Chat as the first comparison anchor." in markdown
    assert (
        "- Compare explicitly against: iTerm2 selected output Add to Chat, Broad lexical bridge."
        in markdown
    )


def test_positioning_anchors_allow_explicit_comparison_priority_override():
    brief = ProjectBrief(
        name="terminal-layer",
        goal="Compare terminal selection prior art before building.",
        keywords=["terminal selection", "add to chat"],
        target_users=["developers"],
        tech_stack=["terminal"],
        exclusions=[],
    )
    candidates = [
        CandidateRepo(
            name="higher-score-close-adjacent",
            url="https://example.com/higher-score-close-adjacent",
            kind="terminal_feature",
            description="Terminal selection add to chat for developers.",
            topics=["terminal-selection", "add-to-chat"],
            attributes={"layer": "A Strongest close adjacent"},
        ),
        CandidateRepo(
            name="manual-anchor",
            url="https://example.com/manual-anchor",
            kind="terminal_feature",
            description="Terminal selection.",
            attributes={
                "layer": "A Strongest close adjacent",
                "comparison_priority": "-1",
            },
        ),
    ]

    report = build_report(
        brief,
        candidates,
        generated_at="2026-06-20T00:00:00+08:00",
    )

    closest = report.to_dict()["differentiation"]["positioning_brief"][
        "closest_alternatives"
    ]
    assert report.candidates[0].name == "higher-score-close-adjacent"
    assert closest[0]["name"] == "manual-anchor"


def test_build_report_adds_actionable_decision_dashboard():
    brief = load_brief(FIXTURES / "brief.json")
    candidates = load_candidates(FIXTURES / "github_repos.json")

    report = build_report(
        brief,
        candidates,
        generated_at="2026-05-24T00:00:00Z",
        search_log=[
            {
                "source": "manual",
                "query": "fixture",
                "result_count": 3,
                "used_count": 3,
                "status": "ok",
                "error": None,
            },
            {
                "source": "github",
                "query": "prior art cli",
                "result_count": 3,
                "used_count": 3,
                "status": "ok",
                "error": None,
            },
        ],
    )
    dashboard = report.to_dict()["decision_dashboard"]

    assert dashboard["go_no_go"] == "review"
    assert dashboard["status"] == "ready_for_manual_review"
    assert "Review" in dashboard["primary_action"]
    assert any("Required source not satisfied: web" in item for item in dashboard["review_queue"])
    assert any("integration cost" in item for item in dashboard["open_questions"])


def test_unknown_adoption_evidence_caps_decision_confidence():
    brief = ProjectBrief(
        name="adoption-review",
        goal="Adopt a matching Python CLI.",
        keywords=["prior art", "report"],
        target_users=["developers"],
        tech_stack=["python"],
        exclusions=[],
    )
    candidates = [
        CandidateRepo(
            name="strong-match",
            url="https://example.com/strong-match",
            kind="repo",
            description="Prior art report CLI for developers.",
            topics=["prior-art", "report", "python"],
            license="MIT",
            language="Python",
            last_update="2026-01-01T00:00:00Z",
        )
    ]

    report = build_report(
        brief,
        candidates,
        generated_at="2026-06-04T00:00:00+00:00",
        search_log=[
            {
                "source": "manual",
                "query": "fixture",
                "result_count": 1,
                "used_count": 1,
                "status": "ok",
                "error": None,
            },
            {
                "source": "github",
                "query": "prior art report cli",
                "result_count": 1,
                "used_count": 1,
                "status": "ok",
                "error": None,
            },
            {
                "source": "web",
                "query": "prior art report cli",
                "result_count": 1,
                "used_count": 1,
                "status": "ok",
                "error": None,
            },
        ],
    )

    records = report.candidates[0].evidence_records
    assert {"category": "license", "status": "known", "source": "candidate_metadata", "detail": "MIT"} in records
    assert any(record["category"] == "integration" and record["status"] == "unknown" for record in records)
    assert report.coverage.confidence == "High"
    assert report.decision.confidence == "Medium"
    assert any("adoption evidence records" in reason for reason in report.decision.confidence_reasons)


def test_discovery_brief_fields_survive_report_generation():
    brief = load_brief(FIXTURES / "discovery_brief.json")
    assert isinstance(brief, DiscoveryBrief)
    candidates = [
        CandidateRepo(
            name="skills.volces.com@github-research",
            url="https://skills.sh/skills.volces.com/github-research",
            description="GitHub research skill with coverage matrix and search log.",
            topics=["skill", "github"],
            language="Markdown",
        ),
        CandidateRepo(
            name="eze-is/web-access",
            url="https://github.com/eze-is/web-access",
            description="Web access helper for agents.",
            topics=["web", "search"],
            language="Python",
        ),
    ]

    report = build_report(
        brief,
        candidates,
        generated_at="2026-05-24T00:00:00Z",
        search_log=[
            {
                "source": "manual",
                "query": "known candidates",
                "result_count": 2,
                "used_count": 2,
                "status": "ok",
                "error": None,
            },
            {
                "source": "github",
                "query": "prior art skill",
                "result_count": 1,
                "used_count": 1,
                "status": "ok",
                "error": None,
            },
            {
                "source": "skills",
                "query": "prior art skill",
                "result_count": 1,
                "used_count": 1,
                "status": "ok",
                "error": None,
            },
        ],
    )
    data = report.to_dict()

    assert data["brief"]["target_type"] == "skill"
    assert data["brief"]["intent"] == "build"
    assert data["brief"]["must_have"] == ["coverage matrix", "search log"]
    assert data["coverage"]["confidence"] == "High"
    assert {"source": "skills", "required": True} in data["coverage"]["source_requirements"]


def test_missing_known_candidate_caps_coverage():
    brief = load_brief(FIXTURES / "discovery_brief.json")
    assert isinstance(brief, DiscoveryBrief)

    report = build_report(
        brief,
        [
            CandidateRepo(
                name="skills.volces.com@github-research",
                url="https://skills.sh/skills.volces.com/github-research",
                description="GitHub research skill with coverage matrix and search log.",
                topics=["skill", "github"],
            )
        ],
        generated_at="2026-05-24T00:00:00Z",
        search_log=[
            {
                "source": "manual",
                "query": "known candidates",
                "result_count": 1,
                "used_count": 1,
                "status": "ok",
                "error": None,
            },
            {
                "source": "github",
                "query": "prior art skill",
                "result_count": 1,
                "used_count": 1,
                "status": "ok",
                "error": None,
            },
            {
                "source": "skills",
                "query": "prior art skill",
                "result_count": 1,
                "used_count": 1,
                "status": "ok",
                "error": None,
            },
        ],
    )

    assert report.coverage.confidence == "Medium"
    assert any("https://github.com/eze-is/web-access" in item for item in report.coverage.blind_spots)


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
    assert report.decision.confidence == "Low"
    assert report.decision.recommendation == "Research More"
    assert any("skills source failed" in item for item in report.coverage.blind_spots)
    assert all("No major source-class blind spots" not in item for item in report.coverage.blind_spots)


def test_write_new_is_report_level_not_candidate_disposition():
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

    report = build_report(
        brief,
        candidates,
        generated_at="2026-05-24T00:00:00Z",
        search_log=[
            {
                "source": "manual",
                "query": "fixture",
                "result_count": 1,
                "used_count": 1,
                "status": "ok",
                "error": None,
            },
            {
                "source": "web",
                "query": "business opportunity discovery tools",
                "result_count": 0,
                "used_count": 0,
                "status": "empty",
                "error": None,
            },
            {
                "source": "github",
                "query": "business opportunity discovery skill",
                "result_count": 0,
                "used_count": 0,
                "status": "empty",
                "error": None,
            },
        ],
    )

    assert report.candidates[0].recommendation == "Monitor"
    assert report.decision.recommendation == "Write New"
    assert "no candidate is sufficient" in report.suggested_updates[0]


def test_empty_candidate_set_produces_partial_research_more_report():
    brief = load_brief(FIXTURES / "brief.json")

    report = build_report(
        brief,
        [],
        generated_at="2026-05-24T00:00:00Z",
        search_log=[
            {
                "source": "github",
                "query": "project discovery cli",
                "result_count": 0,
                "used_count": 0,
                "status": "failed",
                "error": "rate limit",
            }
        ],
    )

    assert report.summary.candidate_count == 0
    assert report.summary.top_recommendation == "Research More"
    assert report.decision.recommendation == "Research More"
    assert report.decision.confidence == "Low"
    assert report.coverage.confidence == "Low"


def test_risks_include_license_and_activity_metadata():
    brief = ProjectBrief(
        name="integration-review",
        goal="Review integration candidates before adopting.",
        keywords=["integration"],
        target_users=["developers"],
        tech_stack=["python"],
        exclusions=[],
    )
    candidates = [
        CandidateRepo(
            name="missing-license",
            url="https://example.com/missing-license",
            description="Python integration helper.",
            topics=["integration"],
            language="Python",
            license="",
            last_update="2026-01-01T00:00:00Z",
        ),
        CandidateRepo(
            name="custom-license",
            url="https://example.com/custom-license",
            description="Python integration helper.",
            topics=["integration"],
            language="Python",
            license="Custom",
            last_update="2026-01-01T00:00:00Z",
        ),
        CandidateRepo(
            name="stale-agpl",
            url="https://example.com/stale-agpl",
            description="Python integration helper.",
            topics=["integration"],
            language="Python",
            license="AGPL-3.0",
            last_update="2022-01-01T00:00:00Z",
        ),
    ]

    report = build_report(
        brief,
        candidates,
        generated_at="2026-06-04T00:00:00+00:00",
    )

    risks = "\n".join(report.risks)
    assert "missing-license: missing license metadata" in risks
    assert "custom-license: license 'Custom' is not recognized as permissive" in risks
    assert "stale-agpl: AGPL license may limit direct adoption" in risks
    assert "stale-agpl: last update is more than 24 months before report generation" in risks


def test_render_markdown_contains_required_sections_and_recommendation():
    brief = load_brief(FIXTURES / "brief.json")
    candidates = load_candidates(FIXTURES / "github_repos.json")
    report = build_report(brief, candidates, generated_at="2026-05-24T00:00:00Z")

    markdown = render_markdown(report)

    for heading in [
        "Executive Summary",
        "Positioning Brief",
        "Decision Dashboard",
        "Search Summary",
        "Source Requirements",
        "Coverage Matrix",
        "Similar Projects",
        "Overlap Matrix",
        "What To Borrow",
        "What To Avoid",
        "Recommendation And Confidence",
        "Coverage Confidence And Blind Spots",
        "Differentiation Map",
        "Differentiation Is Not Enough: Useful Positioning",
        "Risks And Unknowns",
        "Suggested ADR / Backlog Updates",
    ]:
        assert f"## {heading}" in markdown
    assert "sample/prior-art-cli" in markdown
    assert "Recommendation" in markdown


def test_render_markdown_places_decision_dashboard_near_the_top():
    brief = load_brief(FIXTURES / "brief.json")
    candidates = load_candidates(FIXTURES / "github_repos.json")
    report = build_report(
        brief,
        candidates,
        generated_at="2026-05-24T00:00:00Z",
        search_log=[
            {
                "source": "manual",
                "query": "fixture",
                "result_count": 3,
                "used_count": 3,
                "status": "ok",
                "error": None,
            },
            {
                "source": "github",
                "query": "prior art cli",
                "result_count": 3,
                "used_count": 3,
                "status": "ok",
                "error": None,
            },
        ],
    )

    markdown = render_markdown(report)

    assert markdown.index("## Positioning Brief") < markdown.index("## Decision Dashboard")
    assert markdown.index("## Decision Dashboard") < markdown.index("## Search Summary")
    assert "- Go / Hold / Review: **review**." in markdown
    assert "- Review queue: Required source not satisfied: web." in markdown


def test_render_markdown_redacts_local_paths_from_source_errors():
    brief = load_brief(FIXTURES / "brief.json")
    candidates = load_candidates(FIXTURES / "github_repos.json")
    report = build_report(
        brief,
        candidates,
        generated_at="2026-05-24T00:00:00Z",
        search_log=[
            {
                "source": "manual",
                "query": "fixture",
                "result_count": 3,
                "used_count": 3,
                "status": "failed",
                "error": "failed reading /Users/caoyuqi/Documents/private/report.json",
            }
        ],
    )

    markdown = render_markdown(report)

    assert "/Users/caoyuqi/Documents/private/report.json" not in markdown
    assert "[local-path]/report.json" in markdown


def test_render_markdown_replaces_unsafe_candidate_link_urls():
    brief = ProjectBrief(
        name="unsafe-link-review",
        goal="Render a report with untrusted candidate metadata.",
        keywords=["terminal"],
        target_users=["developers"],
        tech_stack=["python"],
        exclusions=[],
    )
    candidates = [
        CandidateRepo(
            name="unsafe-link",
            url="javascript:alert(1)",
            description="Terminal helper for developers.",
            topics=["terminal"],
            language="Python",
        )
    ]

    markdown = render_markdown(
        build_report(
            brief,
            candidates,
            generated_at="2026-06-04T00:00:00+00:00",
        )
    )

    assert "javascript:alert" not in markdown
    assert "[unsafe-link](about:blank)" in markdown


def test_render_markdown_includes_differentiation_map():
    brief = ProjectBrief(
        name="terminal-layer",
        goal="Create a terminal selection layer for existing CLI coding agents.",
        keywords=["terminal selection", "CLI coding agents"],
        target_users=["developers"],
        tech_stack=["iTerm2"],
        exclusions=["generic AI terminal"],
    )
    candidates = [
        CandidateRepo(
            name="close-tool",
            url="https://example.com/close-tool",
            kind="plugin",
            description="Terminal selection helper for AI chat.",
            topics=["terminal selection", "AI chat"],
            attributes={"layer": "B Close adjacent"},
        )
    ]
    report = build_report(brief, candidates, generated_at="2026-06-20T00:00:00+08:00")

    markdown = render_markdown(report)

    assert "## Positioning Brief" in markdown
    assert "- Verdict: **No direct match recorded**." in markdown
    assert "- Closest alternative: close-tool" in markdown
    assert "- Candidate role: close-tool -> integration target" in markdown
    assert "## Differentiation Map" in markdown
    assert "- Commodity feature: terminal selection" in markdown
    assert "- Claim to avoid: Do not position around generic AI terminal." in markdown
    assert "- README positioning draft:" in markdown


def test_render_markdown_escapes_table_and_list_content():
    brief = ProjectBrief(
        name="pipe | brief",
        goal="Review table escaping.",
        keywords=["table"],
        target_users=[],
        tech_stack=["python"],
        exclusions=[],
    )
    candidates = [
        CandidateRepo(
            name="owner/repo | injected",
            url="https://example.com/repo(foo)",
            description="Python table tool.",
            license="MIT | Apache",
            language="Python\nExtra",
        )
    ]
    report = build_report(
        brief,
        candidates,
        generated_at="2026-05-24T00:00:00Z",
        search_log=[
            {
                "source": "manual",
                "query": "table | query\nsecond line",
                "result_count": 1,
                "used_count": 1,
                "status": "ok",
                "error": "note | detail",
            }
        ],
    )

    markdown = render_markdown(report)

    assert "table \\| query second line" in markdown
    assert "MIT \\| Apache" in markdown
    assert "Python Extra" in markdown
    assert "[owner/repo \\| injected](https://example.com/repo%28foo%29)" in markdown


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
