from __future__ import annotations

import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from project_scout.models import CandidateRepo

GITHUB_SEARCH_URL = "https://api.github.com/search/repositories"


def search_github_repositories(query: str, *, limit: int = 10, timeout: int = 20) -> list[CandidateRepo]:
    params = urlencode({"q": query, "per_page": max(1, min(limit, 50))})
    request = Request(
        f"{GITHUB_SEARCH_URL}?{params}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "project-scout",
        },
    )
    with urlopen(request, timeout=timeout) as response:  # noqa: S310 - fixed GitHub API URL.
        payload = json.loads(response.read().decode("utf-8"))
    return parse_github_search_response(payload)


def parse_github_search_response(payload: dict[str, object]) -> list[CandidateRepo]:
    items = payload.get("items", [])
    if not isinstance(items, list):
        raise ValueError("GitHub search response must contain an items list")
    return [_repo_from_item(item) for item in items if isinstance(item, dict)]


def _repo_from_item(item: dict[str, object]) -> CandidateRepo:
    license_data = item.get("license") or {}
    license_name = ""
    if isinstance(license_data, dict):
        license_name = str(license_data.get("spdx_id") or license_data.get("name") or "")
    topics = item.get("topics") or []
    return CandidateRepo(
        name=str(item.get("full_name") or item.get("name") or ""),
        url=str(item.get("html_url") or ""),
        stars=int(item.get("stargazers_count") or 0),
        last_update=str(item.get("updated_at") or ""),
        description=str(item.get("description") or ""),
        topics=[str(topic) for topic in topics] if isinstance(topics, list) else [],
        license=license_name,
        language=str(item.get("language") or ""),
        readme_summary="",
    )
