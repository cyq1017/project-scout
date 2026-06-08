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


def load_score_weights(path: str | Path) -> dict[str, float]:
    data = _read_json(path)
    if not isinstance(data, dict):
        raise ValueError("score weights JSON must be an object")
    return _score_weights({str(key): float(value) for key, value in data.items()})


def build_report(
    brief: ProjectBrief,
    candidates: Iterable[CandidateRepo],
    *,
    generated_at: str | None = None,
    search_log: Iterable[dict[str, object] | SearchLogEntry] | None = None,
    score_weights: dict[str, float] | None = None,
) -> ScoutReport:
    weights = _score_weights(score_weights)
    scored = [_score_candidate(brief, candidate, weights=weights) for candidate in candidates]
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
    generated = generated_at or datetime.now(UTC).replace(microsecond=0).isoformat()
    risks = _risks(scored, generated_at=generated)
    suggested_updates = _suggested_updates(brief, scored)
    top = scored[0].recommendation if scored else "Ignore"
    log_entries = _search_log_entries(search_log)
    decision = _decision_summary(scored, log_entries)
    coverage = _coverage_summary(log_entries)
    return ScoutReport(
        brief=brief,
        generated_at=generated,
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
    for entry in search_log:
        if entry.status == "failed":
            blind_spots.append(f"{entry.source} source failed: {entry.error or 'no error detail recorded'}.")
        elif entry.status == "rate_limited":
            blind_spots.append(f"{entry.source} source was rate-limited.")
    if "web" not in source_names:
        blind_spots.append("Web and community sources were not covered unless supplied manually.")
    if "skills" not in source_names:
        blind_spots.append("Skills registry was not covered unless supplied manually.")
    if not blind_spots:
        blind_spots.append("No major source-class blind spots recorded; still verify primary sources before adoption.")

    return CoverageSummary(
        confidence=confidence,
        sources=sources,
        blind_spots=blind_spots,
        stop_reason="Compared available candidates after recorded source collection.",
    )


def _score_candidate(
    brief: ProjectBrief, candidate: CandidateRepo, *, weights: dict[str, float]
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


def _suggested_updates(brief: ProjectBrief, candidates: list[ScoredCandidate]) -> list[str]:
    top = candidates[0] if candidates else None
    if top is None:
        return [f"ADR: Document why {brief.name} proceeds without comparable candidates."]
    if top.recommendation == "Write New":
        return [
            f"ADR: Record why no candidate is sufficient and Write New is the current recommendation for {top.name}.",
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
