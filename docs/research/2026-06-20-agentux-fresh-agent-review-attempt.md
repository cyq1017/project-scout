# AgentUX Fresh-Agent Review Attempt

Date: 2026-06-20
Milestone: M2 skill quality gate

## Purpose

This note records an attempted fresh-agent run of
`docs/plans/2026-06-20-agentux-dogfood-prompt.md` through Claude Code CLI. The
attempt was meant to test whether `prior-art-scout` transfers to another agent
without hidden local context.

## Environment

- Reviewer command: `/opt/homebrew/bin/claude`
- Version: `2.1.170 (Claude Code)`
- Mode: non-interactive `claude -p`
- Repository state before and after: no tracked file changes from the Claude
  run; only the existing untracked `docs/plans/project-scout-adjustment-plan.md`
  remained.

## Attempt 1

The first constrained run targeted the legacy root `/tmp/agentux-*` artifact
paths from the original dogfood prompt. It returned no terminal output before
being interrupted, but the root `/tmp/agentux-*` files had fresh timestamps and
passed:

```bash
.venv/bin/python scripts/check-agentux-dogfood-artifacts.py --dir /tmp
```

This result is not accepted as clean fresh-agent evidence because previous
`/tmp/agentux-*` artifacts already existed. The run may have read or reused
existing files.

## Attempt 2

A clean directory was created:

```text
/tmp/agentux-fresh-claude.fHidbr
```

Claude was instructed to write only inside that directory and not to read or
reuse root `/tmp/agentux-*` files. The run produced no terminal output and no
files in the clean directory before it was interrupted.

Observed clean-dir state:

```text
agentux-brief.json: missing
agentux-candidates.json: missing
agentux-report.json: missing
agentux-prior-art-map.md: missing
agentux-source-log.md: missing
agentux-chat-summary.md: missing
```

## Conclusion

The local dogfood and artifact checker are useful, but this constrained Claude
CLI setup did not complete a clean fresh-agent run. M2 remains pending until a
fresh agent produces a clean artifact bundle in a new `/tmp` directory and the
bundle passes:

```bash
.venv/bin/python scripts/check-agentux-dogfood-artifacts.py --dir <fresh-output-directory>
```

Then a human or reviewer agent still needs to inspect source quality,
candidate accuracy, blind spots, and unsupported uniqueness claims.
