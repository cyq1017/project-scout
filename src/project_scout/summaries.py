from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from project_scout.models import CandidateRepo


def load_summary_overrides(path: str | Path) -> dict[str, str]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, dict):
        return {str(key): str(value) for key, value in data.items()}
    if not isinstance(data, list):
        raise ValueError("summary overrides JSON must be an object or list")
    overrides: dict[str, str] = {}
    for item in data:
        if not isinstance(item, dict):
            continue
        key = str(item.get("url") or item.get("name") or "")
        summary = str(item.get("summary") or item.get("readme_summary") or "")
        if key and summary:
            overrides[key] = summary
    return overrides


def apply_summary_overrides(
    candidates: list[CandidateRepo], overrides: dict[str, str]
) -> tuple[list[CandidateRepo], int]:
    applied = 0
    updated = []
    for candidate in candidates:
        summary = overrides.get(candidate.url) or overrides.get(candidate.name)
        if summary:
            applied += 1
            updated.append(CandidateRepo(**{**candidate.to_dict(), "readme_summary": summary}))
        else:
            updated.append(candidate)
    return updated, applied
