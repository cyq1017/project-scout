from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from project_scout.models import CandidateRepo


def load_web_candidates(path: str | Path) -> list[CandidateRepo]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("web candidates JSON must be a list")
    return [_web_candidate_from_dict(item) for item in data if isinstance(item, dict)]


def _web_candidate_from_dict(data: dict[str, Any]) -> CandidateRepo:
    title = str(data.get("title") or data.get("name") or data["url"])
    summary = str(data.get("summary") or data.get("readme_summary") or data.get("description") or "")
    topics = data.get("topics") or ["web"]
    kind = str(data.get("kind") or data.get("target_type") or "web")
    attributes = data.get("attributes") if isinstance(data.get("attributes"), dict) else {}
    return CandidateRepo(
        name=title,
        url=str(data["url"]),
        kind=kind,
        description=str(data.get("description") or summary),
        topics=[str(topic) for topic in topics] if isinstance(topics, list) else ["web"],
        license=str(data.get("license", "") or ""),
        language=str(data.get("language", "") or ""),
        readme_summary=summary,
        attributes={str(key): str(value) for key, value in attributes.items()},
    )
