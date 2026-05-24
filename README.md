# project-scout

`project-scout` is a local-first CLI and Python library for prior-art discovery before starting a new project, reworking a major feature, or changing a roadmap.

The MVP focuses on a narrow workflow:

1. Read a project brief from JSON.
2. Import candidate repositories from GitHub search, fixture data, or manual URL lists.
3. Normalize repository metadata.
4. Score overlap with deterministic rules.
5. Write a Markdown prior-art map and a machine-readable JSON report.

It does not log in, store tokens, create issues or pull requests, or make final decisions for the user.

## Install For Development

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e ".[dev]"
```

## Run With Fixtures

```bash
project-scout report \
  --brief tests/fixtures/brief.json \
  --candidates tests/fixtures/github_repos.json \
  --out-json project-scout-report.json \
  --out-md docs/research/2026-05-prior-art-map.md
```

## Import Manual URLs

```bash
project-scout report \
  --brief tests/fixtures/brief.json \
  --urls tests/fixtures/manual_urls.txt \
  --out-json project-scout-report.json \
  --out-md docs/research/2026-05-prior-art-map.md
```

## Search GitHub Without Login

```bash
project-scout report \
  --brief tests/fixtures/brief.json \
  --github-query "prior art github search cli python" \
  --github-limit 10
```

GitHub search uses the unauthenticated REST API and does not store tokens. It may hit public rate limits.
For each GitHub search result, `project-scout` makes a best-effort unauthenticated README request and stores a short deterministic plaintext summary when available.

## Run Tests

```bash
pytest
```

## Non-Goals For MVP

- Autonomous agent behavior.
- Broad web crawling.
- Credential or token storage.
- Automatic issue, PR, or roadmap edits.
- LLM-only scoring or non-repeatable recommendations.
