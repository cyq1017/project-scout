# project-scout

`project-scout` is a local-first CLI, Python library, and skill source repository for prior-art discovery before starting a project, writing a skill/plugin, adopting a tool, reworking a major feature, or changing a roadmap.

The current CLI MVP focuses on a narrow workflow:

1. Read a project brief or discovery brief from JSON.
2. Import candidate repositories and skills from GitHub search, skills registry search, fixture data, or manual URL lists.
3. Normalize candidate metadata while preserving candidate `kind` and source-specific attributes.
4. Score overlap with deterministic rules.
5. Write a Markdown prior-art map and a machine-readable JSON report with search log, coverage confidence, decision confidence, and blind spots.

It does not log in, store tokens, create issues or pull requests, claim
exhaustive discovery, or make final decisions for the user.

The broader skill direction is `prior-art-scout`: a pre-build / pre-adopt discovery gate that can quick-scan or formally compare projects, skills, plugins, tools, MCP servers, products, papers, and internal assets.

## Install For Development

```bash
python3.13 -m venv .venv
. .venv/bin/activate
python -m pip install -e ".[dev]"
```

Python 3.12 or 3.13 is recommended for local development. On macOS, synced
folders such as iCloud Drive can mark editable-install files in `.venv`
`hidden`/`dataless`. CPython skips hidden `.pth` files, which can make the
`project-scout` console script fail to import `project_scout` or make pytest
import hang. Python 3.14 has reproduced this most often, but the durable fix is
to keep the actual venv outside the synced checkout.

```bash
scripts/bootstrap-dev.sh
```

`scripts/bootstrap-dev.sh` creates the real venv under
`${XDG_CACHE_HOME:-$HOME/.cache}/project-scout/venv` by default, links it at
`.venv`, installs `.[dev]`, and runs the fixture smoke gate. Override the venv
location with `PROJECT_SCOUT_VENV_DIR=/path/to/venv` or the parent directory
with `PROJECT_SCOUT_VENV_PARENT=/path/to/parent` if needed.

`scripts/smoke.sh` verifies both the installed console script and the
source-tree fallback. It writes only to `/tmp`.

## Run With Fixtures

After `scripts/smoke.sh` passes, use the console script:

```bash
.venv/bin/project-scout report \
  --brief tests/fixtures/brief.json \
  --candidates tests/fixtures/github_repos.json \
  --out-json /tmp/project-scout-entrypoint.json \
  --out-md /tmp/project-scout-entrypoint.md \
  --generated-at 2026-06-04T00:00:00+00:00
```

For local recovery or import-path troubleshooting, the reliable fallback is the
source-tree module entrypoint. The smoke script writes only to `/tmp`:

```bash
scripts/smoke.sh
```

Equivalent direct command:

```bash
PYTHONPATH=src .venv/bin/python -m project_scout.cli report \
  --brief tests/fixtures/brief.json \
  --candidates tests/fixtures/github_repos.json \
  --out-json /tmp/project-scout-smoke.json \
  --out-md /tmp/project-scout-smoke.md \
  --generated-at 2026-06-04T00:00:00+00:00
```

## Brief Templates

Create a brief from a reusable template, replace the placeholder values, and
pass it to `project-scout report --brief`:

```bash
.venv/bin/project-scout init-brief \
  --template skill \
  --out /tmp/my-skill-brief.json
```

- [skill-discovery.json](examples/brief-templates/skill-discovery.json): evaluate whether to build a reusable agent skill.
- [cli-library.json](examples/brief-templates/cli-library.json): evaluate a small local CLI/library idea.
- [agent-plugin.json](examples/brief-templates/agent-plugin.json): evaluate an agent plugin, connector, or MCP-style integration.

Discovery briefs keep their `target_type`, `intent`, `must_have`,
`nice_to_have`, and `known_candidates` fields in JSON reports. The scoring path
uses an internal normalized view, but the report preserves the original brief so
source requirements and known-candidate blind spots can be audited.

## Source Profiles

Use [source profiles](docs/source-profiles/README.md) to decide which sources
are required before running a report. Profiles are lightweight presets, not
crawler instructions.

Reports include a `source_requirements` coverage section. High coverage requires
the target-specific required sources to be satisfied and all known candidates to
be represented in the candidate set. Missing required sources or known
candidates are recorded as blind spots.

Each scored candidate also includes structured `evidence_records` for license,
maintenance, primary-source URL, integration, and pricing/security. Records can
be `known` or `unknown`; unknown adoption evidence caps decision confidence and
must be resolved by manual primary-source review before relying on the report.

## Sample Reports

- [project-scout fixture JSON report](examples/project-scout-report.json): machine-readable fixture report for the built-in project-scout brief.
- [project-scout fixture prior-art map](docs/research/2026-05-prior-art-map.md): Markdown fixture report for the built-in project-scout brief.
- [商机发现 skill prior-art map](docs/research/2026-05-business-opportunity-skill-prior-art-map.md): 用中文展示如何评估是否值得自研一个商机发现 skill。
- [DeepSeek coding agent desktop prior-art map](docs/research/2026-05-deepseek-coding-agent-desktop-prior-art-map.md): prior-art map for a desktop DeepSeek coding agent direction.

## Import Manual URLs

```bash
project-scout report \
  --brief tests/fixtures/brief.json \
  --urls tests/fixtures/manual_urls.txt \
  --out-json /tmp/project-scout-manual-urls.json \
  --out-md /tmp/project-scout-manual-urls.md
```

## Import Curated Web Candidates

Use curated web candidate JSON for product pages, papers, docs, or externally
reviewed pages. This is an offline adapter; it does not crawl.

```bash
project-scout report \
  --brief tests/fixtures/brief.json \
  --web-candidates tests/fixtures/web_candidates.json \
  --summary-overrides tests/fixtures/summary_overrides.json \
  --out-json /tmp/project-scout-web.json \
  --out-md /tmp/project-scout-web.md
```

`--summary-overrides` is the optional LLM summarization adapter boundary: an
external summarizer may write JSON summaries, and `project-scout` imports them
without calling a model itself.

Curated candidates may include `kind` such as `product`, `paper`, `skill`,
`mcp_server`, or `repo`, plus an `attributes` object for source-specific
metadata. These fields are included in JSON output and considered by the
deterministic relevance text path.

## Configure Scoring Weights

Default scoring is deterministic. Override weights only for local experiments:

```bash
project-scout report \
  --brief tests/fixtures/brief.json \
  --candidates tests/fixtures/github_repos.json \
  --weights tests/fixtures/score_weights_stack.json \
  --out-json /tmp/project-scout-weighted.json \
  --out-md /tmp/project-scout-weighted.md
```

Relevance matching supports ASCII tokens and basic CJK text overlap. This is a
deterministic lexical signal, not semantic translation or LLM scoring.

## Search GitHub Without Login

```bash
project-scout report \
  --brief tests/fixtures/brief.json \
  --github-query "prior art github search cli python" \
  --github-query "project discovery markdown report" \
  --github-limit 10
```

GitHub search uses the unauthenticated REST API and does not store tokens. It may hit public rate limits.
For each GitHub search result, `project-scout` makes a best-effort unauthenticated README request and stores a short deterministic plaintext summary when available.
Pass `--github-query` more than once to run multiple bounded searches; candidates are merged by URL.
If GitHub search fails, the CLI records a failed source entry and still writes a
partial `Research More` report when possible.

## Search Skills Registry

```bash
project-scout report \
  --brief tests/fixtures/discovery_brief.json \
  --skills-query "prior art skill" \
  --candidates tests/fixtures/github_repos.json \
  --out-json examples/prior-art-scout-report.json \
  --out-md docs/research/2026-05-prior-art-scout-map.md
```

Skills registry search shells out to `npx skills find`. If the registry command fails, the formal-gate search log records the failure rather than hiding it.

## Recommendation Semantics

Candidate-level recommendations describe what to do with a specific candidate:
`Adopt`, `Borrow`, `Integrate`, `Fork`, `Extend`, `Avoid`, `Ignore`, or
`Monitor`.

Report-level decisions describe what to do after considering the candidate set
and source coverage. `Write New` is report-level only. Empty candidate sets,
failed sources, or weak coverage produce `Research More` so the report can
document the failed path and blind spots instead of pretending that no useful
prior art exists.

Decision confidence is heuristic, not a probability, and is capped by coverage
confidence and unresolved adoption evidence.

Implementation-wise, candidate relevance still comes from deterministic scoring,
while candidate disposition and report-level decision gates live in
`project_scout.recommendation`.

## Run Tests

```bash
.venv/bin/python -m pytest
```

`scripts/smoke.sh` is the install/entrypoint gate. The pytest suite covers the
library behavior and includes a regression test that invokes
`.venv/bin/project-scout` without `PYTHONPATH`.

The GitHub Actions CI gate runs `scripts/bootstrap-dev.sh` and then
`.venv/bin/python -m pytest`.

## Skill Source

This repository also maintains skill source under `skills/`.

- [skills/prior-art-scout/SKILL.md](skills/prior-art-scout/SKILL.md): reusable discovery skill.
- [docs/skill-repository-strategy.md](docs/skill-repository-strategy.md): how this repo uses skills and adjacent skill orchestration.
- [docs/plans/2026-05-26-prior-art-scout-skill-design.md](docs/plans/2026-05-26-prior-art-scout-skill-design.md): current design plan.
- [docs/patterns/skill-experience-library.md](docs/patterns/skill-experience-library.md): how reusable skill/project lessons are captured without bloating installable skills.

The skill is intended to answer questions such as:

```text
Before I build this, what already exists?
Should I adopt, integrate, fork, extend, borrow from, or write something new?
Are there similar skills/plugins/tools already available?
```

For daily use, install or copy the skill folder into the user-level Codex skills directory. Keep this repository as the source of truth for development and public distribution.

Example local install:

```bash
scripts/install-skill.sh
```

Public GitHub release, registry publication, and community promotion require explicit approval before pushing or publishing.

Conductor integration must stay as an external local CLI/plugin boundary; see
[docs/integrations/conductor-boundary.md](docs/integrations/conductor-boundary.md).

## Experience Library

Reusable lessons from building and testing skills live under `docs/`, separate
from installable skill runtime files:

- `docs/patterns/`: transferable methods and design patterns.
- `docs/case-studies/`: evidence-rich analyses of existing skills, projects, or scans.
- `docs/templates/`: repeatable forms for future discovery and skill design work.
- `docs/source-patterns/`: source-specific search notes and pitfalls.

Only promote a lesson into `skills/*/references/` when an agent needs it during
execution. Keep process history, broad comparisons, and promotion strategy in
repo-level docs.

## Non-Goals For MVP

- Autonomous agent behavior.
- Broad web crawling.
- Credential or token storage.
- Automatic issue, PR, or roadmap edits.
- LLM-only scoring or non-repeatable recommendations.
- Claims that recorded sources prove no other solution exists.
