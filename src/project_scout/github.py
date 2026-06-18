from __future__ import annotations

import base64
import json
import re
from urllib.parse import urlencode
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from project_scout.models import CandidateRepo

GITHUB_SEARCH_URL = "https://api.github.com/search/repositories"
GITHUB_API_URL = "https://api.github.com"


def search_github_repositories(
    query: str,
    *,
    limit: int = 10,
    timeout: int = 20,
    include_readme: bool = True,
) -> list[CandidateRepo]:
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
    candidates = parse_github_search_response(payload)
    if not include_readme:
        return candidates
    return [_with_readme_summary(candidate, timeout=timeout) for candidate in candidates]


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
        kind="repo",
        stars=int(item.get("stargazers_count") or 0),
        last_update=str(item.get("updated_at") or ""),
        description=str(item.get("description") or ""),
        topics=[str(topic) for topic in topics] if isinstance(topics, list) else [],
        license=license_name,
        language=str(item.get("language") or ""),
        readme_summary="",
    )


def _with_readme_summary(candidate: CandidateRepo, *, timeout: int) -> CandidateRepo:
    summary = fetch_readme_summary(candidate.name, timeout=timeout)
    if not summary:
        return candidate
    return CandidateRepo(
        **{**candidate.to_dict(), "readme_summary": summary},
    )


def fetch_readme_summary(full_name: str, *, timeout: int = 20) -> str:
    if "/" not in full_name:
        return ""
    request = Request(
        f"{GITHUB_API_URL}/repos/{full_name}/readme",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "project-scout",
        },
    )
    try:
        with urlopen(request, timeout=timeout) as response:  # noqa: S310 - fixed GitHub API URL.
            payload = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError):
        return ""
    content = payload.get("content", "")
    if not isinstance(content, str):
        return ""
    try:
        text = base64.b64decode(content).decode("utf-8", errors="replace")
    except ValueError:
        return ""
    return summarize_readme_text(text)


def summarize_readme_text(text: str, *, max_chars: int = 400) -> str:
    selected = _section_aware_readme_text(text)
    without_code = re.sub(r"```.*?```", " ", selected, flags=re.DOTALL)
    without_images = re.sub(r"!\[[^\]]*]\([^)]*\)", " ", without_code)
    without_links = re.sub(r"\[([^\]]+)]\([^)]*\)", r"\1", without_images)
    without_markup = re.sub(r"[#>*_`|~]+", " ", without_links)
    collapsed = " ".join(without_markup.split())
    if len(collapsed) <= max_chars:
        return collapsed
    return collapsed[: max_chars - 1].rsplit(" ", 1)[0].rstrip(".") + "."


def _section_aware_readme_text(text: str) -> str:
    sections = _markdown_sections(text)
    if not sections:
        return text
    ranked = sorted(sections, key=lambda section: section[0], reverse=True)
    selected = [body for score, _heading, body in ranked if score > 0]
    if not selected:
        selected = [body for _score, _heading, body in sections]
    return "\n\n".join(selected[:3])


def _markdown_sections(text: str) -> list[tuple[int, str, str]]:
    sections: list[tuple[int, str, str]] = []
    current_heading = ""
    current_lines: list[str] = []

    def flush() -> None:
        body = "\n".join(current_lines).strip()
        if body:
            sections.append((_section_score(current_heading), current_heading, body))

    for line in text.splitlines():
        heading = re.match(r"^\s{0,3}#{1,3}\s+(.+?)\s*$", line)
        if heading:
            flush()
            current_heading = heading.group(1).strip().lower()
            current_lines = [line]
        else:
            current_lines.append(line)
    flush()
    return sections


def _section_score(heading: str) -> int:
    if not heading:
        return 4
    if any(term in heading for term in ["overview", "about", "what", "why"]):
        return 5
    if any(term in heading for term in ["feature", "usage", "example", "quickstart"]):
        return 4
    if any(term in heading for term in ["install", "setup", "configuration"]):
        return 1
    if any(term in heading for term in ["license", "contributing", "changelog", "roadmap"]):
        return 0
    return 2
