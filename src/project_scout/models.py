from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class ProjectBrief:
    name: str
    goal: str
    keywords: list[str]
    target_users: list[str]
    tech_stack: list[str]
    exclusions: list[str]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ProjectBrief":
        return cls(
            name=str(data["name"]),
            goal=str(data["goal"]),
            keywords=_string_list(data.get("keywords", [])),
            target_users=_string_list(data.get("target_users", [])),
            tech_stack=_string_list(data.get("tech_stack", [])),
            exclusions=_string_list(data.get("exclusions", [])),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CandidateRepo:
    name: str
    url: str
    stars: int = 0
    last_update: str = ""
    description: str = ""
    topics: list[str] = field(default_factory=list)
    license: str = ""
    language: str = ""
    readme_summary: str = ""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CandidateRepo":
        return cls(
            name=str(data["name"]),
            url=str(data["url"]),
            stars=int(data.get("stars", 0) or 0),
            last_update=str(data.get("last_update", "") or ""),
            description=str(data.get("description", "") or ""),
            topics=_string_list(data.get("topics", [])),
            license=str(data.get("license", "") or ""),
            language=str(data.get("language", "") or ""),
            readme_summary=str(data.get("readme_summary", "") or ""),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ScoredCandidate(CandidateRepo):
    similarity_score: float = 0.0
    recommendation: str = "Ignore"
    evidence: list[str] = field(default_factory=list)
    avoid_reasons: list[str] = field(default_factory=list)

    @classmethod
    def from_candidate(
        cls,
        candidate: CandidateRepo,
        *,
        similarity_score: float,
        recommendation: str,
        evidence: list[str],
        avoid_reasons: list[str],
    ) -> "ScoredCandidate":
        return cls(
            **candidate.to_dict(),
            similarity_score=similarity_score,
            recommendation=recommendation,
            evidence=evidence,
            avoid_reasons=avoid_reasons,
        )


@dataclass(frozen=True)
class ReportSummary:
    candidate_count: int
    top_recommendation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ScoutReport:
    brief: ProjectBrief
    generated_at: str
    summary: ReportSummary
    candidates: list[ScoredCandidate]
    overlap_matrix: list[dict[str, Any]]
    recommendations: list[dict[str, Any]]
    risks: list[str]
    suggested_updates: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "brief": self.brief.to_dict(),
            "generated_at": self.generated_at,
            "summary": self.summary.to_dict(),
            "candidates": [candidate.to_dict() for candidate in self.candidates],
            "overlap_matrix": self.overlap_matrix,
            "recommendations": self.recommendations,
            "risks": self.risks,
            "suggested_updates": self.suggested_updates,
        }


def _string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise TypeError("expected a list of strings")
    return [str(item) for item in value if str(item).strip()]
