# project-scout

`project-scout` is a local-first CLI, Python library, and skill source repository for prior-art discovery before starting a project, writing a skill/plugin, adopting a tool, reworking a major feature, or changing a roadmap.

The current CLI MVP focuses on a narrow workflow:

1. Read a project brief from JSON.
2. Import candidate repositories from GitHub search, fixture data, or manual URL lists.
3. Normalize repository metadata.
4. Score overlap with deterministic rules.
5. Write a Markdown prior-art map and a machine-readable JSON report.

It does not log in, store tokens, create issues or pull requests, or make final decisions for the user.

The broader skill direction is `prior-art-scout`: a pre-build / pre-adopt discovery gate that can quick-scan or formally compare projects, skills, plugins, tools, MCP servers, products, papers, and internal assets.

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

## Skill Source

This repository also maintains skill source under `skills/`.

- [skills/prior-art-scout/SKILL.md](skills/prior-art-scout/SKILL.md): reusable discovery skill.
- [docs/skill-repository-strategy.md](docs/skill-repository-strategy.md): how this repo uses skills and adjacent skill orchestration.
- [docs/plans/2026-05-26-prior-art-scout-skill-design.md](docs/plans/2026-05-26-prior-art-scout-skill-design.md): current design plan.

The skill is intended to answer questions such as:

```text
Before I build this, what already exists?
Should I adopt, integrate, fork, extend, borrow from, or write something new?
Are there similar skills/plugins/tools already available?
```

For daily use, install or copy the skill folder into the user-level Codex skills directory. Keep this repository as the source of truth for development and public distribution.

## Non-Goals For MVP

- Autonomous agent behavior.
- Broad web crawling.
- Credential or token storage.
- Automatic issue, PR, or roadmap edits.
- LLM-only scoring or non-repeatable recommendations.
