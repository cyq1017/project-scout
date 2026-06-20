# Milestone 3: Source Reliability Gate

Status: Complete
Date: 2026-06-20

## Definition

Milestone 3 means live source adapters are bounded, explicit, and auditable.
`project-scout` does not need GitHub, skills registry, or web access to be
available, but when a live adapter is requested it must either return candidates
or record a source status that explains why coverage is partial.

This milestone does not add crawler behavior, background monitoring, token
storage, logged-in browsing, or automatic follow-up research.

## Acceptance Criteria

- GitHub live search has an explicit CLI timeout.
- GitHub README fetches can be disabled for the most reliable collection path.
- GitHub zero-result searches are recorded as `empty`, not successful coverage
  with hidden absence.
- GitHub adapter failures still produce a failed search-log entry and a partial
  report when the rest of the inputs are valid.
- Skills registry search has an explicit CLI timeout.
- Missing `npx`, timeout, or non-zero skills registry exits are converted into
  runtime errors that the CLI records as failed source entries.
- Fixture tests cover the adapter failure and empty-result behavior without
  depending on live network access.
- README and handoff docs describe the reliable commands and the live-adapter
  caveats.

## Commands

Bounded GitHub search without README fan-out:

```bash
.venv/bin/project-scout report \
  --brief tests/fixtures/brief.json \
  --github-query "prior art github search cli python" \
  --github-limit 10 \
  --github-timeout 10 \
  --no-github-readme \
  --out-json /tmp/project-scout-github.json \
  --out-md /tmp/project-scout-github.md
```

Bounded skills registry search:

```bash
.venv/bin/project-scout report \
  --brief tests/fixtures/discovery_brief.json \
  --skills-query "prior art skill" \
  --skills-timeout 10 \
  --candidates tests/fixtures/github_repos.json \
  --out-json /tmp/project-scout-skills.json \
  --out-md /tmp/project-scout-skills.md
```

Core verification:

```bash
.venv/bin/python -m pytest
scripts/smoke.sh
git diff --check
```

## Completion Boundary

M3 is complete when bounded adapter behavior is covered by fixture tests and the
standard local verification gates pass. It does not require live GitHub or
skills registry availability, and it does not close product-research follow-ups
such as AgentUX community-source discovery or Warp behavior verification.
