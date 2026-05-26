from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse

from project_scout.models import (
    CandidateRepo,
    CoverageSummary,
    DecisionSummary,
    DiscoveryBrief,
    ProjectBrief,
    ReportSummary,
    ScoredCandidate,
    SearchLogEntry,
    ScoutReport,
)

RECOMMENDATIONS = {
    "Adopt",
    "Borrow",
    "Integrate",
    "Fork",
    "Extend",
    "Write New",
    "Avoid",
    "Ignore",
    "Monitor",
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


def load_brief(path: str | Path) -> ProjectBrief:
    data = _read_json(path)
    if not isinstance(data, dict):
        raise ValueError("brief JSON must be an object")
    if "target_type" in data or "users_or_consumers" in data:
        return DiscoveryBrief.from_dict(data).to_project_brief()
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
        candidates.append(CandidateRepo(name=_name_from_url(url), url=url))
    return candidates


def build_report(
    brief: ProjectBrief,
    candidates: Iterable[CandidateRepo],
    *,
    generated_at: str | None = None,
    search_log: Iterable[dict[str, object] | SearchLogEntry] | None = None,
) -> ScoutReport:
    scored = [_score_candidate(brief, candidate) for candidate in candidates]
    scored.sort(key=lambda candidate: candidate.similarity_score, reverse=True)
    matrix = [_matrix_row(brief, candidate) for candidate in scored]
    recommendations = [
        {
            "candidate": candidate.name,
            "recommendation": candidate.recommendation,
            "score": candidate.similarity_score,
            "evidence": candidate.evidence,
        }
        for candidate in scored
    ]
    risks = _risks(scored)
    suggested_updates = _suggested_updates(brief, scored)
    top = scored[0].recommendation if scored else "Ignore"
    log_entries = _search_log_entries(search_log)
    decision = _decision_summary(scored, log_entries)
    coverage = _coverage_summary(log_entries)
    return ScoutReport(
        brief=brief,
        generated_at=generated_at or datetime.now(UTC).replace(microsecond=0).isoformat(),
        summary=ReportSummary(candidate_count=len(scored), top_recommendation=top),
        decision=decision,
        coverage=coverage,
        search_log=log_entries,
        candidates=scored,
        overlap_matrix=matrix,
        recommendations=recommendations,
        risks=risks,
        suggested_updates=suggested_updates,
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


def _decision_summary(
    candidates: list[ScoredCandidate],
    search_log: list[SearchLogEntry],
) -> DecisionSummary:
    top = candidates[0] if candidates else None
    if top is None:
        return DecisionSummary(
            recommendation="Ignore",
            confidence="Low",
            rationale=["No candidates were available for comparison."],
            confidence_reasons=["Candidate set is empty."],
        )

    confidence = "High" if top.similarity_score >= 0.72 else "Medium" if top.similarity_score >= 0.45 else "Low"
    if any(entry.status not in {"ok", "empty"} for entry in search_log):
        confidence = "Medium" if confidence == "High" else confidence
    return DecisionSummary(
        recommendation=top.recommendation,
        confidence=confidence,
        rationale=[
            f"{top.name} has the strongest current score ({top.similarity_score:.3f}).",
            f"Recommendation is based on evidence: {', '.join(top.evidence) if top.evidence else 'limited metadata'}.",
        ],
        confidence_reasons=[
            f"{len(candidates)} candidates compared.",
            "Metadata is deterministic but may need manual source verification.",
        ],
    )


def _coverage_summary(search_log: list[SearchLogEntry]) -> CoverageSummary:
    sources = [entry.to_dict() for entry in search_log]
    statuses = {entry.status for entry in search_log}
    source_names = {entry.source for entry in search_log}
    if any(status in {"failed", "rate_limited"} for status in statuses):
        confidence = "Low"
    elif len(source_names) >= 3:
        confidence = "High"
    else:
        confidence = "Medium"

    blind_spots = []
    if "web" not in source_names:
        blind_spots.append("Web and community sources were not covered unless supplied manually.")
    if "skills" not in source_names:
        blind_spots.append("Skills registry was not covered unless supplied manually.")
    if any(status == "rate_limited" for status in statuses):
        blind_spots.append("At least one source was rate-limited.")
    if not blind_spots:
        blind_spots.append("No major source-class blind spots recorded; still verify primary sources before adoption.")

    return CoverageSummary(
        confidence=confidence,
        sources=sources,
        blind_spots=blind_spots,
        stop_reason="Compared available candidates after recorded source collection.",
    )


def _score_candidate(brief: ProjectBrief, candidate: CandidateRepo) -> ScoredCandidate:
    keyword_hits = _phrase_hits(brief.keywords, _candidate_text(candidate))
    stack_hits = _phrase_hits(brief.tech_stack, _candidate_text(candidate))
    user_hits = _phrase_hits(brief.target_users, _candidate_text(candidate))
    exclusion_hits = _phrase_hits(brief.exclusions, _candidate_text(candidate))
    topic_hits = sorted(_tokens(brief.keywords) & _tokens(candidate.topics))
    text_hits = sorted(_tokens([brief.goal, *brief.keywords]) & _tokens(_text_fields(candidate)))

    score = (
        0.35 * _ratio(keyword_hits, brief.keywords)
        + 0.25 * _ratio(stack_hits, brief.tech_stack)
        + 0.10 * _ratio(user_hits, brief.target_users)
        + 0.15 * min(1.0, len(topic_hits) / 3)
        + 0.15 * min(1.0, len(text_hits) / 8)
    )
    if candidate.language and candidate.language.lower() in _tokens(brief.tech_stack):
        score += 0.05
        stack_hits = sorted(set(stack_hits + [candidate.language.lower()]))
    if exclusion_hits:
        score *= 0.75

    score = round(min(score, 1.0), 3)
    evidence = _evidence(keyword_hits, stack_hits, user_hits, topic_hits, text_hits)
    avoid_reasons = [f"matches exclusion: {hit}" for hit in exclusion_hits]
    recommendation = _recommend(score, candidate, evidence, avoid_reasons)
    return ScoredCandidate.from_candidate(
        candidate,
        similarity_score=score,
        recommendation=recommendation,
        evidence=evidence,
        avoid_reasons=avoid_reasons,
    )


def _recommend(
    score: float,
    candidate: CandidateRepo,
    evidence: list[str],
    avoid_reasons: list[str],
) -> str:
    if avoid_reasons and score < 0.55:
        return "Avoid"
    if score >= 0.82 and _permissive_license(candidate.license):
        return "Adopt"
    if score >= 0.70 and _permissive_license(candidate.license):
        return "Fork"
    if score >= 0.58 and _permissive_license(candidate.license):
        return "Integrate"
    if score >= 0.50:
        return "Borrow"
    if score >= 0.34 and evidence:
        return "Write New"
    if score >= 0.20 and evidence:
        return "Monitor"
    return "Ignore"


def _matrix_row(brief: ProjectBrief, candidate: ScoredCandidate) -> dict[str, object]:
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


def _risks(candidates: list[ScoredCandidate]) -> list[str]:
    risks: list[str] = []
    for candidate in candidates:
        if candidate.avoid_reasons:
            risks.append(f"{candidate.name}: {'; '.join(candidate.avoid_reasons)}")
        if candidate.license.upper().startswith("AGPL"):
            risks.append(f"{candidate.name}: AGPL license may limit direct adoption.")
        if not candidate.last_update:
            risks.append(f"{candidate.name}: missing update metadata.")
    if not risks:
        risks.append("No blocking risks found in fixture metadata; verify licenses and activity before adopting.")
    return risks


def _suggested_updates(brief: ProjectBrief, candidates: list[ScoredCandidate]) -> list[str]:
    top = candidates[0] if candidates else None
    if top is None:
        return [f"ADR: Document why {brief.name} proceeds without comparable candidates."]
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
        candidate.description,
        candidate.language,
        candidate.license,
        candidate.readme_summary,
        *candidate.topics,
    ]


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
        tokens.update(_stem_token(token) for token in re.findall(r"[a-z0-9]+", value.lower()))
    return {token for token in tokens if len(token) > 2 and token not in STOPWORDS}


def _normalize(value: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", value.lower()))


def _permissive_license(license_name: str) -> bool:
    normalized = license_name.lower()
    return any(name in normalized for name in ["mit", "apache", "bsd", "isc", "mpl"])


def _stem_token(token: str) -> str:
    if token == "apis":
        return "api"
    if len(token) > 4 and token.endswith("s") and not token.endswith(("is", "ss", "us")):
        return token[:-1]
    return token
