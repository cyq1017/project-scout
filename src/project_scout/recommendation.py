from __future__ import annotations

from project_scout.models import CoverageSummary, DecisionSummary, ScoredCandidate, SearchLogEntry


def decision_summary(
    candidates: list[ScoredCandidate],
    search_log: list[SearchLogEntry],
    coverage: CoverageSummary,
) -> DecisionSummary:
    top = candidates[0] if candidates else None
    if top is None:
        return DecisionSummary(
            recommendation="Research More",
            confidence="Low",
            rationale=["No candidates were available for comparison."],
            confidence_reasons=[
                "Candidate set is empty.",
                "A partial report can document source attempts and blind spots, but cannot support an adoption decision.",
            ],
        )

    confidence = "High" if top.similarity_score >= 0.72 else "Medium" if top.similarity_score >= 0.45 else "Low"
    if any(entry.status not in {"ok", "empty"} for entry in search_log):
        confidence = "Medium" if confidence == "High" else confidence
    confidence = cap_confidence(confidence, coverage.confidence)

    recommendation = top.recommendation
    rationale = [
        f"{top.name} has the strongest current score ({top.similarity_score:.3f}).",
        f"Recommendation is based on evidence: {', '.join(top.evidence) if top.evidence else 'limited metadata'}.",
    ]
    confidence_reasons = [
        f"{len(candidates)} candidates compared.",
        "Metadata is deterministic but may need manual source verification.",
        f"Coverage confidence caps decision confidence at {coverage.confidence}.",
    ]
    if coverage.confidence == "Low":
        recommendation = "Research More"
        confidence = "Low"
        rationale.append("Coverage is too low to support a build/adopt recommendation.")
        confidence_reasons.append("One or more required source attempts failed or no reliable source completed.")
    if _unknown_evidence_records(top):
        confidence = cap_confidence(confidence, "Medium")
        confidence_reasons.append("One or more adoption evidence records are still unknown.")
    if top.recommendation in {"Monitor", "Ignore"}:
        recommendation = "Write New" if coverage.confidence == "High" else "Research More"
        confidence = cap_confidence("Medium", coverage.confidence)
        if recommendation == "Write New":
            rationale.append("No candidate has enough relevance to adopt, integrate, fork, or borrow from directly.")
            confidence_reasons.append("Write New is a report-level decision, not a candidate disposition.")
        else:
            rationale.append("Candidate relevance is weak and coverage is not high enough to justify Write New.")
            confidence_reasons.append("Weak matches require more source coverage before deciding to build.")
    return DecisionSummary(
        recommendation=recommendation,
        confidence=confidence,
        rationale=rationale,
        confidence_reasons=confidence_reasons,
    )


def candidate_disposition(
    score: float,
    *,
    permissive_license: bool,
    has_evidence: bool,
    has_low_score_avoid_reason: bool,
) -> str:
    if has_low_score_avoid_reason:
        return "Avoid"
    if score >= 0.82 and permissive_license:
        return "Adopt"
    if score >= 0.70 and permissive_license:
        return "Fork"
    if score >= 0.58 and permissive_license:
        return "Integrate"
    if score >= 0.50:
        return "Borrow"
    if score >= 0.20 and has_evidence:
        return "Monitor"
    return "Ignore"


def cap_confidence(confidence: str, coverage_confidence: str) -> str:
    levels = {"Low": 0, "Medium": 1, "High": 2}
    reverse = {value: key for key, value in levels.items()}
    return reverse[min(levels[confidence], levels.get(coverage_confidence, 0))]


def _unknown_evidence_records(candidate: ScoredCandidate) -> list[dict[str, str]]:
    return [record for record in candidate.evidence_records if record["status"] == "unknown"]
