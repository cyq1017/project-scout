import base64
import json
import subprocess
from io import BytesIO
from urllib.error import URLError
from unittest.mock import patch

from project_scout.core import load_url_candidates
from project_scout.github import fetch_readme_summary, parse_github_search_response, summarize_readme_text
from project_scout.summaries import apply_summary_overrides, load_summary_overrides
from project_scout.skills_registry import parse_skills_find_output, search_skills_registry
from project_scout.web import load_web_candidates


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return BytesIO(json.dumps(self.payload).encode("utf-8"))

    def __exit__(self, exc_type, exc_value, traceback):
        return False


def test_load_url_candidates_derives_repo_names_from_manual_urls():
    candidates = load_url_candidates("tests/fixtures/manual_urls.txt")

    assert [candidate.name for candidate in candidates] == [
        "sample/prior-art-cli",
        "ecosyste-ms/repos",
    ]
    assert candidates[0].url == "https://github.com/sample/prior-art-cli"


def test_load_web_candidates_maps_curated_page_metadata():
    candidates = load_web_candidates("tests/fixtures/web_candidates.json")

    assert candidates[0].name == "Official Prior Art Product"
    assert candidates[0].url == "https://example.com/prior-art-product"
    assert candidates[0].topics == ["product", "prior-art", "research"]
    assert candidates[0].readme_summary == "Official product page describing prior-art research workflows."


def test_summary_overrides_update_candidates_by_url():
    candidates = load_web_candidates("tests/fixtures/web_candidates.json")
    overrides = load_summary_overrides("tests/fixtures/summary_overrides.json")

    updated, applied = apply_summary_overrides(candidates, overrides)

    assert applied == 1
    assert updated[0].readme_summary == "LLM-prepared summary from an external offline review."


def test_parse_github_search_response_normalizes_repository_metadata():
    payload = {
        "items": [
            {
                "full_name": "sample/prior-art-cli",
                "html_url": "https://github.com/sample/prior-art-cli",
                "stargazers_count": 128,
                "updated_at": "2026-05-01T09:15:00Z",
                "description": "Python CLI for prior-art reports.",
                "topics": ["prior-art", "cli", "python"],
                "license": {"spdx_id": "MIT"},
                "language": "Python",
            }
        ]
    }

    candidates = parse_github_search_response(payload)

    assert len(candidates) == 1
    assert candidates[0].name == "sample/prior-art-cli"
    assert candidates[0].stars == 128
    assert candidates[0].license == "MIT"
    assert candidates[0].readme_summary == ""


def test_summarize_readme_text_extracts_meaningful_plaintext():
    readme = """# prior-art-cli

[![build](https://example.com/badge.svg)](https://example.com)

Python CLI for prior-art research.

It compares GitHub repositories, scores overlap, and exports JSON plus Markdown reports.

```bash
project-scout report --brief brief.json
```
"""

    summary = summarize_readme_text(readme, max_chars=200)

    assert summary == (
        "prior-art-cli Python CLI for prior-art research. It compares GitHub repositories, "
        "scores overlap, and exports JSON plus Markdown reports."
    )


def test_fetch_readme_summary_decodes_github_api_content():
    content = base64.b64encode(b"# sample\n\nPython CLI report generator.").decode("ascii")

    with patch("project_scout.github.urlopen", return_value=FakeResponse({"content": content})):
        summary = fetch_readme_summary("sample/prior-art-cli")

    assert summary == "sample Python CLI report generator."


def test_fetch_readme_summary_returns_empty_string_on_network_failure():
    with patch("project_scout.github.urlopen", side_effect=URLError("rate limited")):
        summary = fetch_readme_summary("sample/prior-art-cli")

    assert summary == ""


def test_parse_skills_find_output_extracts_skill_candidates():
    output = """
Install with npx skills add <owner/repo@skill>

product-on-purpose/pm-skills@discover-competitive-analysis 162 installs
└ https://skills.sh/product-on-purpose/pm-skills/discover-competitive-analysis

skills.volces.com@github-research 25 installs
└ https://skills.sh/skills.volces.com/github-research
"""

    candidates = parse_skills_find_output(output)

    assert [candidate.name for candidate in candidates] == [
        "product-on-purpose/pm-skills@discover-competitive-analysis",
        "skills.volces.com@github-research",
    ]
    assert candidates[0].url == "https://skills.sh/product-on-purpose/pm-skills/discover-competitive-analysis"
    assert candidates[0].topics == ["skill", "skills-registry"]
    assert candidates[0].stars == 162


def test_parse_skills_find_output_strips_ansi_codes_and_k_installs():
    output = """
\x1b[38;5;145mphuryn/pm-skills@competitor-analysis\x1b[0m \x1b[36m1.2K installs\x1b[0m
\x1b[38;5;102m└ https://skills.sh/phuryn/pm-skills/competitor-analysis\x1b[0m
"""

    candidates = parse_skills_find_output(output)

    assert candidates[0].name == "phuryn/pm-skills@competitor-analysis"
    assert candidates[0].url == "https://skills.sh/phuryn/pm-skills/competitor-analysis"
    assert candidates[0].stars == 1200


def test_search_skills_registry_converts_timeout_to_runtime_error():
    with patch("project_scout.skills_registry.subprocess.run", side_effect=subprocess.TimeoutExpired("npx", 1)):
        try:
            search_skills_registry("prior art", timeout=1)
        except RuntimeError as exc:
            assert "timed out" in str(exc)
        else:
            raise AssertionError("expected RuntimeError")
