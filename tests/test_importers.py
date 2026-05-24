from project_scout.core import load_url_candidates
from project_scout.github import parse_github_search_response, summarize_readme_text


def test_load_url_candidates_derives_repo_names_from_manual_urls():
    candidates = load_url_candidates("tests/fixtures/manual_urls.txt")

    assert [candidate.name for candidate in candidates] == [
        "sample/prior-art-cli",
        "ecosyste-ms/repos",
    ]
    assert candidates[0].url == "https://github.com/sample/prior-art-cli"


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
