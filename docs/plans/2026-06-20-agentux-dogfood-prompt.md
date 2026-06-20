# AgentUX Dogfood Prompt

Use this prompt in a fresh agent session to test whether `prior-art-scout`
transfers without hidden context.

Do not include expected findings in the prompt. The evaluator should discover
candidates, source gaps, and positioning implications from the skill and public
sources.

```text
Use prior-art-scout at /Users/caoyuqi/Documents/New project/project-scout/skills/prior-art-scout to run a Formal Gate.

Target:
AgentUX is a selection-aware terminal UX layer for CLI coding agents. First
phase starts with iTerm2: a user selects text in an iTerm2 Claude Code, Codex
CLI, Aider, or similar terminal session; an Add / Branch action appears near
the selection or in a context menu. Add injects the selected terminal output as
structured context into the current CLI agent input. Branch opens a separate
side discussion carrying minimal context: selected text, cwd, git branch or
commit, source session, and originating agent.

The search should focus on whether anyone has already built this combination:

1. capture terminal output selection;
2. provide an AI action near the terminal selection or context menu;
3. inject selected text into an existing CLI coding agent session;
4. support add-to-conversation, ask-about-selection, branch discussion, or side
   thread;
5. work through iTerm2 plugin/script, tmux integration, terminal plugin, macOS
   overlay, IDE-to-terminal bridge, or CLI-agent UX layer.

Use the skill's query matrix, source routing, coverage protocol,
cross-agent protocol, and positioning discussion references. Use public sources
available in this agent runtime. Use `project-scout` CLI/library if available;
if it is not available, record that as a process gap rather than hand-writing
engine-owned fields as final.

Write draft artifacts under /tmp:

- /tmp/agentux-brief.json
- /tmp/agentux-candidates.json
- /tmp/agentux-prior-art-map.md
- /tmp/agentux-report.json
- /tmp/agentux-source-log.md
- /tmp/agentux-chat-summary.md

The chat summary should include:

- whether there is a direct competitor;
- top direct or close matches;
- broad adjacent tools;
- coverage confidence and blind spots;
- go/review/hold dashboard status if a project-scout report was generated;
- AgentUX differentiation and claims to avoid;
- one next validation step.

Keep all outputs local. Do not push, publish, create issues, open PRs, or store
tokens.
```

## Evaluation Notes

After the fresh-agent run, inspect whether the agent:

- applied multiple query families instead of one generic search;
- represented known source gaps honestly;
- prepared structured candidates;
- used `project-scout` when available;
- separated search findings from positioning discussion;
- avoided unsupported uniqueness claims.
