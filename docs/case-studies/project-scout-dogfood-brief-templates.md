# Project-Scout Dogfood: Brief Templates

## Goal

Use `project-scout` itself to make new scout runs faster without expanding the
MVP into a crawler platform.

## Local Workflow

Create a draft brief from a template:

```bash
.venv/bin/project-scout init-brief \
  --template skill \
  --out /tmp/project-scout-dogfood-skill-brief.json
```

Edit the placeholder fields, then run a fixture-first report:

```bash
.venv/bin/project-scout report \
  --brief /tmp/project-scout-dogfood-skill-brief.json \
  --candidates tests/fixtures/github_repos.json \
  --out-json /tmp/project-scout-dogfood-report.json \
  --out-md /tmp/project-scout-dogfood-report.md
```

When a live source is appropriate, keep it bounded:

```bash
.venv/bin/project-scout report \
  --brief /tmp/project-scout-dogfood-skill-brief.json \
  --github-query "prior art skill discovery agent" \
  --github-query "build vs adopt cli" \
  --github-limit 10 \
  --out-json /tmp/project-scout-dogfood-github.json \
  --out-md /tmp/project-scout-dogfood-github.md
```

## Source Profile

For a reusable skill, start with:

- `docs/source-profiles/product.md` when comparing user-facing products.
- `docs/source-profiles/mcp-server.md` when the skill wraps an integration.
- `docs/source-profiles/market-opportunity.md` when the question is whether the
  workflow is worth building at all.

## Notes

- Keep smoke and dogfood outputs in `/tmp` unless the result is deliberately
  curated into `examples/` or `docs/research/`.
- Prefer fixture candidates for regression tests.
- Record missing live sources as blind spots instead of hiding them.
