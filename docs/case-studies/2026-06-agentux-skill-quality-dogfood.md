# AgentUX Skill Quality Dogfood

Date: 2026-06-20
Milestone: M2 skill quality gate

## Purpose

This dogfood run tested whether `prior-art-scout` can guide an AgentUX prior-art
formal gate through search orchestration, engine-backed reporting, and
positioning discussion.

AgentUX target:

- capture terminal output selection;
- show AI action near the terminal selection or context menu;
- inject selected text into an existing CLI coding agent session;
- support Add to current conversation;
- support Branch or side-thread discussion with selected text, cwd, git state,
  source session, and originating agent.

## Local Artifacts

Draft artifacts were written under `/tmp`:

- `/tmp/agentux-brief.json`
- `/tmp/agentux-known-candidates.json`
- `/tmp/agentux-candidates.json`
- `/tmp/agentux-source-log.md`
- `/tmp/agentux-report.json`
- `/tmp/agentux-prior-art-map.md`
- `/tmp/agentux-chat-summary.md`

The engine command used the local `project-scout` console script:

```bash
.venv/bin/project-scout report \
  --brief /tmp/agentux-brief.json \
  --candidates /tmp/agentux-known-candidates.json \
  --web-candidates /tmp/agentux-candidates.json \
  --github-query "Claude Code iTerm2 plugin" \
  --github-query "terminal selection AI assistant" \
  --github-query "tmux copy mode AI assistant" \
  --github-limit 5 \
  --out-json /tmp/agentux-report.json \
  --out-md /tmp/agentux-prior-art-map.md \
  --generated-at 2026-06-20T00:00:00+08:00
```

## Results

`project-scout` generated a report with:

- `20` candidates reviewed;
- report-level decision: `Write New`;
- decision confidence: `Medium`;
- coverage confidence: `High`;
- dashboard state: `review`;
- top comparison anchor: `Send to iTerm2 Claude Code`.

No direct match was recorded for the complete AgentUX combination. The closest
clusters were:

- IDE/editor selection sent to Claude Code terminal;
- ChatGPT desktop reading terminal selected text;
- AI terminal command-output actions;
- terminal APIs and issue threads that expose selection/context-menu
  implementation constraints.

## Source-Profile Lesson

The first engine run used curated web candidates only. For `target_type:
product`, `project-scout` requires both `manual` and `web` sources, so the
dashboard correctly stayed at `hold` because the manual source requirement was
not satisfied.

The second run added a manual known-candidate file. That satisfied the manual
source class, cleared the known-candidate mismatch for `VS Code terminal inline
chat`, and moved the dashboard to `review`.

Lesson for the skill:

- curated web candidates should satisfy the web source class;
- user-provided or manually confirmed candidates should be passed as a manual
  known-candidate file;
- do not let one curated candidate file silently stand in for every source
  class.

## Remaining Gaps

- Skills registry was not covered unless supplied manually.
- npm/PyPI/Homebrew were not formally searched.
- Reddit/Hacker News/blog coverage was partial and should be deepened before
  public uniqueness claims.
- Primary-source verification remains needed for Send to iTerm2 Claude Code and
  ChatGPT Work with Apps behavior.

## Skill Quality Assessment

The new M2 references helped in three ways:

- `query-matrix.md` forced multiple query families instead of one generic
  search.
- `cross-agent-protocol.md` kept the workflow engine-backed and local-first.
- `positioning-discussion.md` separated search findings from build-wedge
  discussion.

The main improvement from this run is the source-profile correction now recorded
in `skills/prior-art-scout/references/source-routing.md`.
