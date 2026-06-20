from __future__ import annotations

import json
import re
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse

from project_scout.models import (
    CandidateRepo,
    CoverageSummary,
    DecisionDashboard,
    DecisionSummary,
    DifferentiationSummary,
    DiscoveryBrief,
    NormalizedBrief,
    ProjectBrief,
    ReportSummary,
    ScoredCandidate,
    SearchLogEntry,
    ScoutReport,
)
from project_scout.recommendation import candidate_disposition, decision_summary

RECOMMENDATIONS = {
    "Adopt",
    "Borrow",
    "Integrate",
    "Fork",
    "Extend",
    "Avoid",
    "Ignore",
    "Monitor",
}
DEFAULT_SCORE_WEIGHTS = {
    "keyword": 0.35,
    "stack": 0.25,
    "user": 0.10,
    "topic": 0.15,
    "text": 0.15,
    "language_bonus": 0.05,
    "exclusion_multiplier": 0.75,
}
STOPWORDS = {
    "and",
    "are",
    "for",
    "from",
    "into",
    "the",
    "that",
    "this",
    "with",
}


def load_brief(path: str | Path) -> ProjectBrief | DiscoveryBrief:
    data = _read_json(path)
    if not isinstance(data, dict):
        raise ValueError("brief JSON must be an object")
    if "target_type" in data or "users_or_consumers" in data:
        return DiscoveryBrief.from_dict(data)
    return ProjectBrief.from_dict(data)


def load_candidates(path: str | Path) -> list[CandidateRepo]:
    data = _read_json(path)
    if not isinstance(data, list):
        raise ValueError("candidate JSON must be a list")
    return [CandidateRepo.from_dict(item) for item in data]


def load_url_candidates(path: str | Path) -> list[CandidateRepo]:
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    candidates: list[CandidateRepo] = []
    for line in lines:
        url = line.strip()
        if not url or url.startswith("#"):
            continue
        candidates.append(CandidateRepo(name=_name_from_url(url), url=url, kind=_kind_from_url(url)))
    return candidates


def load_score_weights(path: str | Path) -> dict[str, float]:
    data = _read_json(path)
    if not isinstance(data, dict):
        raise ValueError("score weights JSON must be an object")
    return _score_weights({str(key): float(value) for key, value in data.items()})


def build_report(
    brief: ProjectBrief | DiscoveryBrief,
    candidates: Iterable[CandidateRepo],
    *,
    generated_at: str | None = None,
    search_log: Iterable[dict[str, object] | SearchLogEntry] | None = None,
    score_weights: dict[str, float] | None = None,
) -> ScoutReport:
    normalized_brief = _normalize_brief(brief)
    weights = _score_weights(score_weights)
    scored = [_score_candidate(normalized_brief, candidate, weights=weights) for candidate in candidates]
    scored.sort(key=lambda candidate: candidate.similarity_score, reverse=True)
    matrix = [_matrix_row(normalized_brief, candidate) for candidate in scored]
    recommendations = [
        {
            "candidate": candidate.name,
            "recommendation": candidate.recommendation,
            "score": candidate.similarity_score,
            "evidence": candidate.evidence,
        }
        for candidate in scored
    ]
    generated = generated_at or datetime.now(UTC).replace(microsecond=0).isoformat()
    log_entries = _search_log_entries(search_log)
    coverage = _coverage_summary(log_entries, normalized_brief, scored)
    decision = decision_summary(scored, log_entries, coverage)
    differentiation = _differentiation_summary(normalized_brief, scored, decision)
    decision_dashboard = _decision_dashboard(normalized_brief, scored, decision, coverage)
    risks = _risks(scored, generated_at=generated)
    suggested_updates = _suggested_updates(normalized_brief, scored, decision)
    top = decision.recommendation
    return ScoutReport(
        brief=brief,
        generated_at=generated,
        summary=ReportSummary(candidate_count=len(scored), top_recommendation=top),
        decision=decision,
        decision_dashboard=decision_dashboard,
        coverage=coverage,
        differentiation=differentiation,
        search_log=log_entries,
        candidates=scored,
        overlap_matrix=matrix,
        recommendations=recommendations,
        risks=risks,
        suggested_updates=suggested_updates,
    )


def _decision_dashboard(
    brief: NormalizedBrief,
    candidates: list[ScoredCandidate],
    decision: DecisionSummary,
    coverage: CoverageSummary,
) -> DecisionDashboard:
    go_no_go = _dashboard_go_no_go(decision, coverage)
    status = _dashboard_status(go_no_go)
    top = candidates[0] if candidates else None
    return DecisionDashboard(
        status=status,
        go_no_go=go_no_go,
        primary_action=_primary_action(brief, top, decision, go_no_go),
        review_queue=_review_queue(coverage, top),
        open_questions=_open_questions(top, coverage),
    )


def _dashboard_go_no_go(decision: DecisionSummary, coverage: CoverageSummary) -> str:
    if decision.recommendation == "Research More" or coverage.confidence == "Low":
        return "hold"
    if decision.confidence == "High" and coverage.confidence == "High":
        return "go"
    return "review"


def _dashboard_status(go_no_go: str) -> str:
    if go_no_go == "hold":
        return "needs_more_research"
    if go_no_go == "go":
        return "ready_for_action"
    return "ready_for_manual_review"


def _primary_action(
    brief: NormalizedBrief,
    top: ScoredCandidate | None,
    decision: DecisionSummary,
    go_no_go: str,
) -> str:
    if go_no_go == "hold":
        return "Resolve source coverage and candidate gaps before making a build/adopt decision."
    if decision.recommendation == "Write New":
        return f"Review the build wedge for {brief.name} against the closest alternatives before roadmap commitment."
    if top is None:
        return "Review source coverage before acting on the report."
    return f"Review {top.name} before acting on the {decision.recommendation} recommendation."


def _review_queue(coverage: CoverageSummary, top: ScoredCandidate | None) -> list[str]:
    queue = [item for item in coverage.blind_spots if item]
    if top is not None:
        queue.append(f"Check primary docs and README evidence for {top.name}.")
        for record in top.evidence_records:
            if record["status"] == "unknown":
                queue.append(f"Verify {record['category'].replace('_', ' ')} for {top.name}: {record['detail']}.")
    return _dedupe(queue)[:8]


def _open_questions(top: ScoredCandidate | None, coverage: CoverageSummary) -> list[str]:
    questions: list[str] = []
    if top is None:
        questions.append("Which candidate sources should be added before this report is decision-ready?")
    else:
        unknown_categories = {record["category"] for record in top.evidence_records if record["status"] == "unknown"}
        if "integration" in unknown_categories:
            questions.append(f"What is the integration cost and API compatibility for {top.name}?")
        if "pricing_security" in unknown_categories:
            questions.append(f"Are pricing, data handling, and security constraints acceptable for {top.name}?")
        if "license" in unknown_categories:
            questions.append(f"What license constraints apply to {top.name}?")
        if "maintenance" in unknown_categories:
            questions.append(f"Is {top.name} actively maintained enough for the intended use?")
    if coverage.confidence != "High":
        questions.append("Which required source gaps must be closed before stronger positioning claims?")
    return _dedupe(questions)[:6]


def _differentiation_summary(
    brief: NormalizedBrief,
    candidates: list[ScoredCandidate],
    decision: DecisionSummary,
) -> DifferentiationSummary:
    commodity_features = _commodity_features(candidates)
    unique_combination = _unique_combination(brief, candidates)
    candidate_roles = _candidate_roles(candidates)
    return DifferentiationSummary(
        positioning_brief=_positioning_brief(brief, candidates, decision, unique_combination),
        candidate_roles=candidate_roles,
        similarity_clusters=_similarity_clusters(candidates),
        commodity_features=commodity_features,
        unique_combination=unique_combination,
        defensible_positioning=_defensible_positioning(brief, candidates, decision),
        claims_to_avoid=_claims_to_avoid(brief, commodity_features),
        borrow_integrate_compete_guidance=_borrow_integrate_compete_guidance(candidates, candidate_roles),
        readme_positioning_draft=_readme_positioning_draft(brief),
    )


def _positioning_brief(
    brief: NormalizedBrief,
    candidates: list[ScoredCandidate],
    decision: DecisionSummary,
    unique_combination: list[str],
) -> dict[str, object]:
    closest = _closest_alternatives(candidates)
    return {
        "verdict": _positioning_verdict(candidates),
        "closest_alternatives": closest,
        "differentiation_claim": unique_combination[0],
        "recommended_positioning": _readme_positioning_draft(brief),
        "decision": decision.recommendation,
        "next_validation_steps": _next_validation_steps(brief, candidates, decision),
    }


def _positioning_verdict(candidates: list[ScoredCandidate]) -> str:
    if not candidates:
        return "No candidates recorded"
    top = candidates[0]
    if top.similarity_score >= 0.82:
        return "Direct match likely"
    if top.similarity_score >= 0.58:
        return "Strong adjacent match recorded"
    return "No direct match recorded"


def _closest_alternatives(candidates: list[ScoredCandidate]) -> list[dict[str, object]]:
    return [
        {
            "name": candidate.name,
            "url": candidate.url,
            "kind": candidate.kind,
            "score": candidate.similarity_score,
            "role": _candidate_role(candidate),
            "why_it_matters": _candidate_role_reason(candidate),
        }
        for candidate in candidates[:3]
    ]


def _candidate_roles(candidates: list[ScoredCandidate]) -> list[dict[str, object]]:
    return [
        {
            "candidate": candidate.name,
            "role": _candidate_role(candidate),
            "reason": _candidate_role_reason(candidate),
        }
        for candidate in candidates[:8]
    ]


def _candidate_role(candidate: ScoredCandidate) -> str:
    explicit = str(candidate.attributes.get("role") or "").strip()
    if explicit:
        return explicit
    if candidate.similarity_score >= 0.82:
        return "competitor"
    if candidate.kind in {"api", "plugin", "jetbrains_plugin", "raycast_extension", "ide_feature", "macos_app"}:
        return "integration target" if candidate.similarity_score >= 0.20 else "prior art"
    if candidate.kind in {"product", "terminal_feature"} and candidate.similarity_score >= 0.58:
        return "competitor"
    return "prior art"


def _candidate_role_reason(candidate: ScoredCandidate) -> str:
    role = _candidate_role(candidate)
    evidence = ", ".join(candidate.evidence[:3]) if candidate.evidence else candidate.kind
    if role == "competitor":
        return f"High similarity around {evidence}; compare positioning and adoption barriers directly."
    if role == "integration target":
        return f"Useful adjacent surface around {evidence}; inspect whether it can be integrated or borrowed from."
    return f"Useful prior-art signal around {evidence}; cite it when narrowing claims."


def _next_validation_steps(
    brief: NormalizedBrief,
    candidates: list[ScoredCandidate],
    decision: DecisionSummary,
) -> list[str]:
    steps = [
        "Verify source coverage against the required source profile before making a uniqueness claim.",
        "Check primary docs for the closest alternatives before writing README positioning.",
    ]
    if candidates:
        steps.append(f"Manually compare the workflow against {candidates[0].name}.")
    if decision.recommendation == "Research More":
        steps.append("Resolve blind spots before using Write New or direct adoption language.")
    if brief.known_candidates:
        steps.append("Confirm every known candidate appears in the candidate set or document why it was excluded.")
    return steps


def _similarity_clusters(candidates: list[ScoredCandidate]) -> list[dict[str, object]]:
    clusters: dict[str, list[ScoredCandidate]] = {}
    for candidate in candidates:
        label = str(candidate.attributes.get("layer") or "").strip()
        if not label:
            if candidate.similarity_score >= 0.58:
                label = "High similarity"
            elif candidate.similarity_score >= 0.34:
                label = "Close adjacent"
            elif candidate.similarity_score >= 0.20:
                label = "Broad adjacent"
            else:
                label = "Low relevance"
        clusters.setdefault(label, []).append(candidate)
    rows = []
    for label, grouped in clusters.items():
        rows.append(
            {
                "label": label,
                "candidates": [candidate.name for candidate in grouped[:6]],
                "highest_score": max(candidate.similarity_score for candidate in grouped),
            }
        )
    return rows


def _commodity_features(candidates: list[ScoredCandidate]) -> list[str]:
    counts: Counter[str] = Counter()
    for candidate in candidates:
        counts.update(feature for feature in candidate.evidence if _useful_positioning_feature(feature))
    features = [
        feature
        for feature, _count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    ]
    return features[:8]


def _useful_positioning_feature(feature: str) -> bool:
    return " " in feature or _contains_cjk(feature) or len(feature) > 3


def _unique_combination(
    brief: NormalizedBrief,
    candidates: list[ScoredCandidate],
) -> list[str]:
    core_requirements = brief.must_have or [*brief.keywords[:4], *brief.tech_stack[:2]]
    if not core_requirements:
        return ["Unique combination is unknown until the brief records core requirements."]
    joined = "; ".join(core_requirements[:5])
    if not candidates:
        return [f"No candidates were available to test the core combination: {joined}."]
    top_score = candidates[0].similarity_score
    if top_score < 0.58:
        return [f"No recorded candidate combines all core requirements: {joined}."]
    return [f"Differentiate through the combined workflow, not a single feature: {joined}."]


def _defensible_positioning(
    brief: NormalizedBrief,
    candidates: list[ScoredCandidate],
    decision: DecisionSummary,
) -> list[str]:
    rows = [
        "Frame differentiation as a combination claim, not a uniqueness claim.",
        (
            f"Position {brief.name} around the {brief.target_type} workflow it enables; "
            "compare directly against the closest recorded candidates."
        ),
    ]
    if decision.recommendation == "Research More":
        rows.append("Keep positioning provisional until required sources and primary evidence are reviewed.")
    if candidates:
        rows.append(f"Use {candidates[0].name} as the first comparison anchor.")
    return rows


def _claims_to_avoid(brief: NormalizedBrief, commodity_features: list[str]) -> list[str]:
    claims = [f"Do not position around {item}." for item in brief.exclusions]
    claims.extend(
        f"Do not claim {feature} is unique without primary-source evidence."
        for feature in _claimworthy_features(commodity_features)[:3]
    )
    if not claims:
        claims.append("Do not claim exhaustive discovery from recorded sources alone.")
    return claims


def _claimworthy_features(features: list[str]) -> list[str]:
    phrase_features = [feature for feature in features if " " in feature or _contains_cjk(feature)]
    return phrase_features or features


def _borrow_integrate_compete_guidance(
    candidates: list[ScoredCandidate],
    candidate_roles: list[dict[str, object]],
) -> list[str]:
    if not candidates:
        return ["Gather candidates before deciding what to borrow, integrate, or compete against."]
    roles_by_name = {str(item["candidate"]): str(item["role"]) for item in candidate_roles}
    rows = []
    for candidate in candidates[:5]:
        evidence = ", ".join(candidate.evidence[:4]) if candidate.evidence else candidate.kind
        role = roles_by_name.get(candidate.name, "prior art")
        rows.append(
            f"Treat {candidate.name} as {role}: inspect {evidence} before claiming differentiation."
        )
    return rows


def _readme_positioning_draft(brief: NormalizedBrief) -> str:
    target_users = ", ".join(brief.target_users[:2]) if brief.target_users else "target users"
    if "existing cli coding agents" in brief.goal.lower():
        target_users = "existing CLI coding agents"
    core_requirements = brief.must_have or brief.keywords[:3]
    core = ", ".join(core_requirements[:3]) if core_requirements else "the recorded workflow"
    exclusion = f" It is not {brief.exclusions[0]}." if brief.exclusions else ""
    return (
        f"{brief.name} is a {brief.target_type} for {target_users} that combines {core}. "
        "It should be evaluated against recorded prior art and does not claim exhaustive discovery."
        f"{exclusion}"
    )


def _normalize_brief(brief: ProjectBrief | DiscoveryBrief) -> NormalizedBrief:
    if isinstance(brief, DiscoveryBrief):
        return NormalizedBrief(
            name=brief.name,
            goal=f"{brief.goal} Target type: {brief.target_type}. Intent: {brief.intent}.",
            keywords=_dedupe([*brief.keywords, *brief.must_have, *brief.nice_to_have]),
            target_users=brief.users_or_consumers,
            tech_stack=_dedupe([*brief.ecosystems, *brief.must_have]),
            exclusions=brief.exclusions,
            target_type=brief.target_type,
            intent=brief.intent,
            must_have=brief.must_have,
            nice_to_have=brief.nice_to_have,
            known_candidates=brief.known_candidates,
        )
    return NormalizedBrief(
        name=brief.name,
        goal=brief.goal,
        keywords=brief.keywords,
        target_users=brief.target_users,
        tech_stack=brief.tech_stack,
        exclusions=brief.exclusions,
    )


def _search_log_entries(
    search_log: Iterable[dict[str, object] | SearchLogEntry] | None,
) -> list[SearchLogEntry]:
    if not search_log:
        return [
            SearchLogEntry(
                source="manual",
                query="unspecified",
                result_count=0,
                used_count=0,
                status="unknown",
                error=None,
            )
        ]
    entries: list[SearchLogEntry] = []
    for entry in search_log:
        if isinstance(entry, SearchLogEntry):
            entries.append(entry)
        elif isinstance(entry, dict):
            entries.append(SearchLogEntry.from_dict(entry))
    return entries


def _coverage_summary(
    search_log: list[SearchLogEntry],
    brief: NormalizedBrief,
    candidates: list[ScoredCandidate],
) -> CoverageSummary:
    sources = [entry.to_dict() for entry in search_log]
    statuses = {entry.status for entry in search_log}
    source_names = {entry.source for entry in search_log}
    ok_sources = {entry.source for entry in search_log if entry.status in {"ok", "empty"}}
    source_requirements = _source_requirements(brief)
    required_sources = {item["source"] for item in source_requirements if item["required"]}
    satisfied_required_sources = required_sources & ok_sources
    missing_required_sources = required_sources - ok_sources
    known_candidate_misses = _missing_known_candidates(brief.known_candidates, candidates)
    if any(status in {"failed", "rate_limited"} for status in statuses):
        confidence = "Low"
    elif not ok_sources:
        confidence = "Low"
    elif not missing_required_sources and not known_candidate_misses:
        confidence = "High"
    elif satisfied_required_sources:
        confidence = "Medium"
    else:
        confidence = "Low"

    blind_spots = []
    for entry in search_log:
        if entry.status == "failed":
            blind_spots.append(f"{entry.source} source failed: {entry.error or 'no error detail recorded'}.")
        elif entry.status == "rate_limited":
            blind_spots.append(f"{entry.source} source was rate-limited.")
    if "web" not in source_names:
        blind_spots.append("Web and community sources were not covered unless supplied manually.")
    if "github" not in source_names:
        blind_spots.append("GitHub repository search was not covered unless supplied manually.")
    if "skills" not in source_names:
        blind_spots.append("Skills registry was not covered unless supplied manually.")
    for source in sorted(missing_required_sources):
        blind_spots.append(f"Required source not satisfied: {source}.")
    for known_candidate in known_candidate_misses:
        blind_spots.append(f"Known candidate was not included in candidate set: {known_candidate}.")
    if not blind_spots:
        blind_spots.append("No major source-class blind spots recorded; still verify primary sources before adoption.")

    return CoverageSummary(
        confidence=confidence,
        sources=sources,
        blind_spots=blind_spots,
        stop_reason="Compared available candidates after recorded source collection.",
        source_requirements=source_requirements,
    )


def _source_requirements(brief: NormalizedBrief) -> list[dict[str, object]]:
    target_type = brief.target_type.lower()
    required = ["manual", "github", "web"]
    optional = ["skills"]
    if target_type == "skill":
        required = ["manual", "github", "skills"]
        optional = ["web"]
    elif target_type in {"product", "market_opportunity"}:
        required = ["manual", "web"]
        optional = ["github", "skills"]
    elif target_type in {"paper", "research"}:
        required = ["manual", "web"]
        optional = ["github", "skills"]
    rows = [{"source": source, "required": True} for source in required]
    rows.extend({"source": source, "required": False} for source in optional)
    return rows


def _missing_known_candidates(
    known_candidates: list[str],
    candidates: list[ScoredCandidate],
) -> list[str]:
    candidate_text = " ".join(
        f"{candidate.name} {candidate.url}".lower() for candidate in candidates
    )
    missing = []
    for known_candidate in known_candidates:
        if known_candidate.lower() not in candidate_text:
            missing.append(known_candidate)
    return missing


def _score_candidate(
    brief: NormalizedBrief, candidate: CandidateRepo, *, weights: dict[str, float]
) -> ScoredCandidate:
    keyword_hits = _phrase_hits(brief.keywords, _candidate_text(candidate))
    stack_hits = _phrase_hits(brief.tech_stack, _candidate_text(candidate))
    user_hits = _phrase_hits(brief.target_users, _candidate_text(candidate))
    exclusion_hits = _phrase_hits(brief.exclusions, _candidate_text(candidate))
    topic_hits = sorted(_tokens(brief.keywords) & _tokens(candidate.topics))
    text_hits = sorted(_tokens([brief.goal, *brief.keywords]) & _tokens(_text_fields(candidate)))

    score = (
        weights["keyword"] * _ratio(keyword_hits, brief.keywords)
        + weights["stack"] * _ratio(stack_hits, brief.tech_stack)
        + weights["user"] * _ratio(user_hits, brief.target_users)
        + weights["topic"] * min(1.0, len(topic_hits) / 3)
        + weights["text"] * min(1.0, len(text_hits) / 8)
    )
    if candidate.language and candidate.language.lower() in _tokens(brief.tech_stack):
        score += weights["language_bonus"]
        stack_hits = sorted(set(stack_hits + [candidate.language.lower()]))
    if exclusion_hits:
        score *= weights["exclusion_multiplier"]

    score = round(min(score, 1.0), 3)
    evidence = _evidence(keyword_hits, stack_hits, user_hits, topic_hits, text_hits)
    avoid_reasons = [f"matches exclusion: {hit}" for hit in exclusion_hits]
    recommendation = _recommend(score, candidate, evidence, avoid_reasons)
    evidence_records = _evidence_records(candidate)
    return ScoredCandidate.from_candidate(
        candidate,
        similarity_score=score,
        recommendation=recommendation,
        evidence=evidence,
        evidence_records=evidence_records,
        avoid_reasons=avoid_reasons,
    )


def _evidence_records(candidate: CandidateRepo) -> list[dict[str, str]]:
    return [
        {
            "category": "license",
            "status": "known" if candidate.license else "unknown",
            "source": "candidate_metadata",
            "detail": candidate.license or "missing license metadata",
        },
        {
            "category": "maintenance",
            "status": "known" if candidate.last_update else "unknown",
            "source": "candidate_metadata",
            "detail": candidate.last_update or "missing update metadata",
        },
        {
            "category": "primary_source",
            "status": "known" if candidate.url else "unknown",
            "source": "candidate_metadata",
            "detail": candidate.url or "missing canonical URL",
        },
        {
            "category": "integration",
            "status": "unknown",
            "source": "manual_verification_required",
            "detail": "integration cost and API compatibility are not automatically verified",
        },
        {
            "category": "pricing_security",
            "status": "unknown",
            "source": "manual_verification_required",
            "detail": "pricing, data handling, and security posture are not automatically verified",
        },
    ]


def _recommend(
    score: float,
    candidate: CandidateRepo,
    evidence: list[str],
    avoid_reasons: list[str],
) -> str:
    return candidate_disposition(
        score,
        permissive_license=_permissive_license(candidate.license),
        has_evidence=bool(evidence),
        has_low_score_avoid_reason=bool(avoid_reasons and score < 0.55),
    )


def _score_weights(overrides: dict[str, float] | None) -> dict[str, float]:
    weights = dict(DEFAULT_SCORE_WEIGHTS)
    if not overrides:
        return weights
    unknown = set(overrides) - set(DEFAULT_SCORE_WEIGHTS)
    if unknown:
        raise ValueError(f"unknown score weight(s): {', '.join(sorted(unknown))}")
    for key, value in overrides.items():
        if value < 0:
            raise ValueError(f"score weight {key} must be non-negative")
        weights[key] = value
    if not 0 <= weights["exclusion_multiplier"] <= 1:
        raise ValueError("score weight exclusion_multiplier must be between 0 and 1")
    return weights


def _matrix_row(brief: NormalizedBrief, candidate: ScoredCandidate) -> dict[str, object]:
    text = _candidate_text(candidate)
    return {
        "candidate": candidate.name,
        "score": candidate.similarity_score,
        "recommendation": candidate.recommendation,
        "keyword_overlap": len(_phrase_hits(brief.keywords, text)),
        "stack_overlap": len(_phrase_hits(brief.tech_stack, text)),
        "user_overlap": len(_phrase_hits(brief.target_users, text)),
        "exclusion_overlap": len(_phrase_hits(brief.exclusions, text)),
        "stars": candidate.stars,
        "last_update": candidate.last_update,
    }


def _risks(candidates: list[ScoredCandidate], *, generated_at: str) -> list[str]:
    risks: list[str] = []
    generated_date = _parse_datetime(generated_at)
    for candidate in candidates:
        if candidate.avoid_reasons:
            risks.append(f"{candidate.name}: {'; '.join(candidate.avoid_reasons)}")
        normalized_license = candidate.license.strip()
        if not normalized_license:
            risks.append(f"{candidate.name}: missing license metadata; verify adoption constraints.")
        elif normalized_license.upper().startswith("AGPL"):
            risks.append(f"{candidate.name}: AGPL license may limit direct adoption.")
        elif not _permissive_license(normalized_license):
            risks.append(
                f"{candidate.name}: license '{normalized_license}' is not recognized as permissive; verify adoption constraints."
            )
        if not candidate.last_update:
            risks.append(f"{candidate.name}: missing update metadata.")
        elif _is_stale(candidate.last_update, generated_date):
            risks.append(
                f"{candidate.name}: last update is more than 24 months before report generation; verify maintenance activity."
            )
    if not risks:
        risks.append("No blocking risks found in fixture metadata; verify licenses and activity before adopting.")
    return risks


def _parse_datetime(value: str) -> datetime | None:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def _is_stale(last_update: str, generated_at: datetime | None) -> bool:
    if generated_at is None:
        return False
    updated_at = _parse_datetime(last_update)
    if updated_at is None:
        return False
    if updated_at.tzinfo is None:
        updated_at = updated_at.replace(tzinfo=UTC)
    if generated_at.tzinfo is None:
        generated_at = generated_at.replace(tzinfo=UTC)
    return (generated_at - updated_at).days > 730


def _suggested_updates(
    brief: NormalizedBrief,
    candidates: list[ScoredCandidate],
    decision: DecisionSummary,
) -> list[str]:
    top = candidates[0] if candidates else None
    if top is None:
        return [
            f"ADR: Record why {brief.name} needs more research before a build/adopt decision.",
            "Backlog: Add at least one candidate source or document why sources were unavailable.",
        ]
    if decision.recommendation == "Write New":
        return [
            f"ADR: Record why no candidate is sufficient and Write New is the current report-level recommendation for {brief.name}.",
            "Backlog: Add manual review tasks for license, maintenance activity, and integration cost.",
            "Backlog: Track borrowed ideas separately from differentiating product decisions.",
        ]
    return [
        f"ADR: Record why {top.recommendation} is the current recommendation for {top.name}.",
        "Backlog: Add manual review tasks for license, maintenance activity, and integration cost.",
        "Backlog: Track borrowed ideas separately from differentiating product decisions.",
    ]


def _evidence(*groups: list[str]) -> list[str]:
    values: list[str] = []
    seen: set[str] = set()
    for group in groups:
        for item in group:
            normalized = item.lower()
            if normalized not in seen:
                values.append(normalized)
                seen.add(normalized)
    return values[:12]


def _read_json(path: str | Path) -> object:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _dedupe(values: list[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        normalized = value.lower()
        if normalized not in seen:
            result.append(value)
            seen.add(normalized)
    return result


def _name_from_url(url: str) -> str:
    parsed = urlparse(url)
    parts = [part for part in parsed.path.split("/") if part]
    if parsed.netloc.endswith("github.com") and len(parts) >= 2:
        return f"{parts[0]}/{parts[1]}"
    return url.rstrip("/").rsplit("/", 1)[-1]


def _candidate_text(candidate: CandidateRepo) -> str:
    return " ".join(_text_fields(candidate))


def _text_fields(candidate: CandidateRepo) -> list[str]:
    return [
        candidate.name,
        candidate.kind,
        candidate.description,
        candidate.language,
        candidate.license,
        candidate.readme_summary,
        *candidate.topics,
        *candidate.attributes.values(),
    ]


def _kind_from_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.netloc.endswith("github.com"):
        return "repo"
    return "web"


def _phrase_hits(needles: list[str], haystack: str) -> list[str]:
    normalized = _normalize(haystack)
    haystack_tokens = _tokens([haystack])
    hits = []
    for needle in needles:
        phrase = _normalize(needle)
        phrase_tokens = _tokens([phrase])
        if phrase and (phrase in normalized or phrase_tokens.issubset(haystack_tokens)):
            hits.append(phrase)
    return sorted(set(hits))


def _ratio(hits: list[str], values: list[str]) -> float:
    if not values:
        return 0.0
    return min(1.0, len(hits) / len(values))


def _tokens(values: Iterable[str]) -> set[str]:
    tokens: set[str] = set()
    for value in values:
        for token in re.findall(r"[a-z0-9]+", value.lower()):
            tokens.add(_stem_token(token))
        for block in re.findall(r"[\u3400-\u9fff]+", value):
            tokens.add(block)
            tokens.update(block[index : index + 2] for index in range(len(block) - 1))
    return {
        token
        for token in tokens
        if (len(token) > 2 or _contains_cjk(token)) and token not in STOPWORDS
    }


def _normalize(value: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+|[\u3400-\u9fff]+", value.lower()))


def _contains_cjk(value: str) -> bool:
    return bool(re.search(r"[\u3400-\u9fff]", value))


def _permissive_license(license_name: str) -> bool:
    normalized = license_name.lower()
    return any(name in normalized for name in ["mit", "apache", "bsd", "isc", "mpl"])


def _stem_token(token: str) -> str:
    if token == "apis":
        return "api"
    if len(token) > 4 and token.endswith("s") and not token.endswith(("is", "ss", "us")):
        return token[:-1]
    return token
