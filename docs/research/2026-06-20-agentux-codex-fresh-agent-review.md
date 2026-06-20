# AgentUX Codex Fresh-Agent Review

Date: 2026-06-20
Milestone: M2 skill quality gate
Reviewer: Codex CLI fresh `exec` session

## Run

The successful clean fresh-agent run wrote artifacts under:

```text
/tmp/agentux-fresh-codex.0a91v5
```

Artifact bundle:

- `/tmp/agentux-fresh-codex.0a91v5/agentux-brief.json`
- `/tmp/agentux-fresh-codex.0a91v5/agentux-candidates.json`
- `/tmp/agentux-fresh-codex.0a91v5/agentux-prior-art-map.md`
- `/tmp/agentux-fresh-codex.0a91v5/agentux-report.json`
- `/tmp/agentux-fresh-codex.0a91v5/agentux-source-log.md`
- `/tmp/agentux-fresh-codex.0a91v5/agentux-chat-summary.md`

The run used a fresh output directory and did not read or reuse old
`/tmp/agentux-*` artifacts.

## Verification

The bundle passed the repo checker:

```bash
.venv/bin/python scripts/check-agentux-dogfood-artifacts.py --dir /tmp/agentux-fresh-codex.0a91v5
```

Observed result:

```text
PASS AgentUX dogfood artifacts
```

The generated `project-scout` report contained:

- `7` candidates;
- report recommendation: `Research More`;
- decision confidence: `Low`;
- dashboard: `hold`;
- coverage confidence: `Low`;
- `6` search-log entries;
- source log, query matrix, structured candidates, engine report, blind spots,
  and positioning discussion with claims to avoid.

## Fresh-Agent Findings

The fresh run changed the competitive picture compared with the local dogfood
run. The strongest close match is now:

```text
Warp Agent Platform: blocks as context and third-party CLI agents
```

The fresh reviewer found primary-source Warp docs for:

- terminal output blocks as agent context;
- third-party CLI agent support, including Claude Code and Codex;
- selection-as-context from Warp editor or review surfaces;
- conversation forking.

The run still did not verify a full exact match for AgentUX's proposed
combination:

- arbitrary selected terminal text in iTerm2;
- Add or Branch action near the terminal selection or context menu;
- injection into an already-running CLI coding agent session;
- side discussion carrying selected text, cwd, git branch or commit, source
  session, and originating agent.

## Skill Transfer Assessment

M2 accepted for the skill-quality gate.

Evidence:

- The fresh agent loaded `prior-art-scout` and its references.
- The query matrix was applied across direct, synonym, ecosystem, shape,
  negative, and adjacent query families.
- The agent prepared structured candidates.
- The agent used `project-scout` for deterministic report generation.
- The agent noticed an initial source-profile mismatch and reran the engine
  with `--web-candidates`, preserving the M2 source-routing lesson.
- The agent recorded unavailable sources as gaps instead of treating them as
  negative evidence.
- The chat summary separated search findings from positioning advice and
  listed claims to avoid.

## Remaining Gaps

These are follow-up source or runtime gaps, not blocking M2 skill-protocol gaps:

- GitHub adapter failed DNS resolution in the Codex CLI shell runtime.
- skills registry search timed out.
- Community sources such as Reddit, Hacker News, and forums were not deeply
  covered.
- Warp behavior still needs hands-on verification to confirm whether arbitrary
  terminal text selection, not only terminal blocks or editor selections, can
  be attached to a third-party CLI agent session.

## Completion Judgment

M2 can close because the fresh-agent dogfood run produced the required artifact
bundle, surfaced coverage limitations honestly, used the deterministic engine,
and did not reveal a blocking skill-protocol gap. The remaining gaps are
recorded as narrower follow-up tasks.
