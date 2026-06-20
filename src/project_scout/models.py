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
class DiscoveryBrief:
    name: str
    target_type: str
    intent: str
    goal: str
    keywords: list[str]
    users_or_consumers: list[str]
    ecosystems: list[str]
    must_have: list[str]
    nice_to_have: list[str]
    exclusions: list[str]
    known_candidates: list[str]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DiscoveryBrief":
        return cls(
            name=str(data["name"]),
            target_type=str(data.get("target_type", "project") or "project"),
            intent=str(data.get("intent", "research") or "research"),
            goal=str(data["goal"]),
            keywords=_string_list(data.get("keywords", [])),
            users_or_consumers=_string_list(data.get("users_or_consumers", [])),
            ecosystems=_string_list(data.get("ecosystems", [])),
            must_have=_string_list(data.get("must_have", [])),
            nice_to_have=_string_list(data.get("nice_to_have", [])),
            exclusions=_string_list(data.get("exclusions", [])),
            known_candidates=_string_list(data.get("known_candidates", [])),
        )

    def to_project_brief(self) -> ProjectBrief:
        return ProjectBrief(
            name=self.name,
            goal=f"{self.goal} Target type: {self.target_type}. Intent: {self.intent}.",
            keywords=_dedupe([*self.keywords, *self.must_have, *self.nice_to_have]),
            target_users=self.users_or_consumers,
            tech_stack=_dedupe([*self.ecosystems, *self.must_have]),
            exclusions=self.exclusions,
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class NormalizedBrief:
    name: str
    goal: str
    keywords: list[str]
    target_users: list[str]
    tech_stack: list[str]
    exclusions: list[str]
    target_type: str = "project"
    intent: str = "research"
    must_have: list[str] = field(default_factory=list)
    nice_to_have: list[str] = field(default_factory=list)
    known_candidates: list[str] = field(default_factory=list)

    def to_project_brief(self) -> ProjectBrief:
        return ProjectBrief(
            name=self.name,
            goal=self.goal,
            keywords=self.keywords,
            target_users=self.target_users,
            tech_stack=self.tech_stack,
            exclusions=self.exclusions,
        )


@dataclass(frozen=True)
class CandidateRepo:
    name: str
    url: str
    kind: str = "repo"
    stars: int = 0
    last_update: str = ""
    description: str = ""
    topics: list[str] = field(default_factory=list)
    license: str = ""
    language: str = ""
    readme_summary: str = ""
    attributes: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "CandidateRepo":
        return cls(
            name=str(data["name"]),
            url=str(data["url"]),
            kind=str(data.get("kind", "repo") or "repo"),
            stars=int(data.get("stars", 0) or 0),
            last_update=str(data.get("last_update", "") or ""),
            description=str(data.get("description", "") or ""),
            topics=_string_list(data.get("topics", [])),
            license=str(data.get("license", "") or ""),
            language=str(data.get("language", "") or ""),
            readme_summary=str(data.get("readme_summary", "") or ""),
            attributes=_string_dict(data.get("attributes", {})),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ScoredCandidate(CandidateRepo):
    similarity_score: float = 0.0
    recommendation: str = "Ignore"
    evidence: list[str] = field(default_factory=list)
    evidence_records: list[dict[str, str]] = field(default_factory=list)
    avoid_reasons: list[str] = field(default_factory=list)

    @classmethod
    def from_candidate(
        cls,
        candidate: CandidateRepo,
        *,
        similarity_score: float,
        recommendation: str,
        evidence: list[str],
        evidence_records: list[dict[str, str]],
        avoid_reasons: list[str],
    ) -> "ScoredCandidate":
        return cls(
            **candidate.to_dict(),
            similarity_score=similarity_score,
            recommendation=recommendation,
            evidence=evidence,
            evidence_records=evidence_records,
            avoid_reasons=avoid_reasons,
        )


@dataclass(frozen=True)
class ReportSummary:
    candidate_count: int
    top_recommendation: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DecisionSummary:
    recommendation: str
    confidence: str
    rationale: list[str] = field(default_factory=list)
    confidence_reasons: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DecisionDashboard:
    status: str
    go_no_go: str
    primary_action: str
    review_queue: list[str] = field(default_factory=list)
    open_questions: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SearchLogEntry:
    source: str
    query: str
    result_count: int
    used_count: int
    status: str
    error: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SearchLogEntry":
        return cls(
            source=str(data["source"]),
            query=str(data.get("query", "")),
            result_count=int(data.get("result_count", 0) or 0),
            used_count=int(data.get("used_count", 0) or 0),
            status=str(data.get("status", "ok") or "ok"),
            error=str(data["error"]) if data.get("error") else None,
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CoverageSummary:
    confidence: str
    sources: list[dict[str, Any]]
    blind_spots: list[str]
    stop_reason: str
    source_requirements: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DifferentiationSummary:
    positioning_brief: dict[str, Any]
    candidate_roles: list[dict[str, Any]]
    similarity_clusters: list[dict[str, Any]]
    commodity_features: list[str]
    unique_combination: list[str]
    defensible_positioning: list[str]
    claims_to_avoid: list[str]
    borrow_integrate_compete_guidance: list[str]
    readme_positioning_draft: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ScoutReport:
    brief: ProjectBrief | DiscoveryBrief
    generated_at: str
    summary: ReportSummary
    decision: DecisionSummary
    decision_dashboard: DecisionDashboard
    coverage: CoverageSummary
    differentiation: DifferentiationSummary
    search_log: list[SearchLogEntry]
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
            "decision": self.decision.to_dict(),
            "decision_dashboard": self.decision_dashboard.to_dict(),
            "coverage": self.coverage.to_dict(),
            "differentiation": self.differentiation.to_dict(),
            "search_log": [entry.to_dict() for entry in self.search_log],
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


def _string_dict(value: Any) -> dict[str, str]:
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise TypeError("expected a dict of string attributes")
    return {str(key): str(item) for key, item in value.items() if str(item).strip()}


def _dedupe(values: list[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        normalized = value.lower()
        if normalized not in seen:
            result.append(value)
            seen.add(normalized)
    return result
