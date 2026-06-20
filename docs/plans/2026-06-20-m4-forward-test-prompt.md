# M4 Forward-Test Prompt

Use this prompt in a fresh agent session after M4 implementation. Do not include
expected findings or previous AgentUX conclusions.

```text
Use the prior-art-scout skill at:
/Users/caoyuqi/Documents/New project/project-scout/skills/prior-art-scout

Run a Formal Gate technical due-diligence review for this target:

AgentUX is a selection-aware terminal UX layer for CLI coding agents. The first
phase starts with iTerm2: when a user selects terminal output from a Claude Code,
Codex CLI, Aider, Gemini CLI, or similar coding-agent session, AgentUX should
surface Add and Branch actions. Add injects the selected text as structured
context into the current agent input. Branch should open an independent branch
conversation that inherits the selected text, cwd, git branch/commit, and source
session context.

Focus on whether similar projects or products already combine:

1. terminal output selection capture;
2. AI action UI near the terminal selection or in a terminal context menu;
3. injection of selected text into an existing CLI coding-agent session;
4. Add to conversation, ask about selection, branch discussion, or side thread;
5. iTerm2 plugin, tmux integration, terminal plugin, macOS overlay,
   IDE-to-terminal bridge, or CLI-agent UX layer.

Use the skill's technical due-diligence process. Keep the search bounded and
auditable. Do not claim exhaustive discovery. Do not treat AI terminal products
as direct matches unless they reuse or augment existing CLI coding-agent
sessions through terminal selection context.

Write artifacts under:
/tmp/project-scout-m4-forward-<agent>-<timestamp>

Required artifacts:

- discovery brief JSON;
- source log or source-log Markdown;
- query family notes;
- structured candidate JSON;
- project-scout report JSON;
- Markdown report;
- positioning discussion;
- evidence-gap checklist;
- self-review against:
  /Users/caoyuqi/Documents/New project/project-scout/docs/milestones/m4-skill-pack-due-diligence-gate.md

If a source adapter fails or a tool is unavailable, record the failure and
continue with fallback sources. If project-scout cannot run, write a provisional
report and mark the missing engine as a process gap.

Final chat response should include:

- artifact directory;
- top recommendation;
- decision confidence;
- coverage confidence;
- go/review/hold status;
- top direct or close candidates;
- strongest claims to avoid;
- next validation step.
```
