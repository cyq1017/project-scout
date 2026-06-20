# Milestone 2: Skill Quality Gate

Status: Local dogfood complete, fresh-agent review pending
Date: 2026-06-20

## Definition

Milestone 2 means `prior-art-scout` can be used by another capable agent with
limited local context and still produce a defensible prior-art workflow:
searched sources, structured candidates, engine-backed report generation, and a
useful positioning discussion.

M2 does not require every source to be available. It requires unavailable
sources to be visible in the source log, coverage matrix, or blind spots.

## Acceptance Criteria

- The skill includes references for query matrix, positioning discussion, and
  cross-agent execution.
- Search quality is guided by query families, target-specific source routing,
  known-candidate recall, source log requirements, and stop rules.
- Discussion quality is guided by report fields, candidate evidence,
  positioning claims to avoid, counterarguments, and next validation steps.
- Cross-agent stability is guided by capability names, tool-neutral fallback
  rules, and `project-scout` engine use when available.
- A fresh-agent AgentUX dogfood prompt exists and writes draft artifacts to
  `/tmp`.
- The dogfood run produces or explains the absence of:
  - source log;
  - query matrix use;
  - structured candidates;
  - `project-scout` report;
  - coverage confidence and blind spots;
  - positioning discussion with claims to avoid.
- The repo still avoids crawler behavior, hosted services, token storage,
  default logged-in browsing, automatic roadmap mutation, and public publishing.

## Required Verification

Run:

```bash
.venv/bin/python -m pytest
scripts/smoke.sh
git diff --check
```

For install or package-facing changes, also run the wheel install smoke from
`docs/milestones/m1-local-prior-art-gate.md`.

## Forward-Test Gate

Use:

```text
docs/plans/2026-06-20-agentux-dogfood-prompt.md
```

The forward-test should run in a fresh agent session where possible. Do not pass
the expected answer. Review the produced artifacts against this milestone after
the run.

After artifacts are written under `/tmp`, run:

```bash
.venv/bin/python scripts/check-agentux-dogfood-artifacts.py --dir /tmp
```

The checker is a bundle-shape gate only. It confirms the fresh-agent run
produced the expected local files and engine-backed fields, but it does not
prove candidate accuracy or source completeness.

## Local Dogfood Result

The first local dogfood run is recorded in:

```text
docs/case-studies/2026-06-agentux-skill-quality-dogfood.md
```

It produced `/tmp` draft artifacts, generated a `project-scout` report for
AgentUX, and exposed one skill-protocol fix: curated web candidates should not
silently stand in for manual known-candidate coverage when the source profile
requires both source classes.

## Completion Boundary

M2 is complete when the AgentUX dogfood run reveals no blocking skill-protocol
gaps, or when every remaining gap is recorded as a narrower follow-up task.
