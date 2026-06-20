# AgentUX Focused Follow-Up

Date: 2026-06-20
Scope: M4 follow-up for small-plugin prior art, Warp primary docs, and iTerm2
Add-mechanics feasibility.

## Artifact Bundle

The refreshed `project-scout` report is local-only:

```text
/tmp/project-scout-agentux-focused-followup.json
/tmp/project-scout-agentux-focused-followup.md
/tmp/project-scout-agentux-focused-web-candidates.json
```

Command:

```bash
.venv/bin/project-scout report \
  --brief /tmp/project-scout-m4-forward-codex-20260620T154153+0800/agentux-brief.json \
  --candidates /tmp/project-scout-m4-forward-codex-20260620T154153+0800/agentux-candidates.json \
  --web-candidates /tmp/project-scout-agentux-focused-web-candidates.json \
  --github-query "iTerm2 selection Claude Code plugin" \
  --github-query "tmux copy mode AI assistant Claude Code Codex" \
  --github-query "selected terminal text AI assistant" \
  --github-query "Claude Code iTerm2 plugin" \
  --github-limit 8 \
  --github-timeout 15 \
  --no-github-readme \
  --skills-query "iTerm2 Claude Code terminal selection" \
  --skills-timeout 15 \
  --out-json /tmp/project-scout-agentux-focused-followup.json \
  --out-md /tmp/project-scout-agentux-focused-followup.md \
  --generated-at 2026-06-20T00:00:00+08:00
```

## Report Result

The refreshed report covered manual, web, GitHub, and skills-registry sources:

- candidates reviewed: 36;
- report-level recommendation: Write New;
- decision confidence: Medium;
- coverage confidence: High;
- dashboard: review / ready_for_manual_review;
- source blind spot: no major source-class blind spot recorded, but primary
  sources still need verification before adoption claims.

This is not a uniqueness claim. It means the recorded sources still did not
show one project combining the full AgentUX workflow:

- terminal output selection capture;
- Add or Branch action near the selection or in a terminal context menu;
- injection into an existing CLI coding-agent session;
- Add to current conversation or side-thread discussion;
- inherited selected text, cwd, git branch/commit, and source session context.

## Added Source Evidence

Focused follow-up added these evidence classes:

- Claude Code side-chat feature request:
  https://github.com/anthropics/claude-code/issues/48099
  - close prior art for selecting REPL output and opening a read-only side chat
    with inherited session/project context.
- Warp Blocks as Context:
  https://docs.warp.dev/agent-platform/local-agents/agent-context/blocks-as-context/
  - close prior art for attaching terminal blocks as structured agent context.
- Warp Conversation Forking:
  https://docs.warp.dev/agent-platform/local-agents/interacting-with-agents/conversation-forking/
  - close prior art for forked agent conversations and inherited context.
- unitmux:
  https://dev.to/ugo/unitmux-a-floating-desktop-app-for-claude-code-and-codex-in-tmux-54gn
  - close adjacent overlay for sending instructions to Claude Code or Codex in
    tmux.
- CCB:
  https://github.com/SeemSeam/claude_codex_bridge
  - broad/close adjacent multi-agent CLI workspace with real CLI panes and
    worktree/session orchestration.
- Windows Terminal Chat:
  https://learn.microsoft.com/en-us/windows/terminal/terminal-chat
  - broad adjacent terminal chat prior art.
- Claude Code iTerm2 Tab Alert:
  https://github.com/STRML/cc-iterm2-tab-alert
  - close adjacent iTerm2 plus Claude Code plugin proof, but notification/state
    UX rather than selected-output context injection.
- HN discussion:
  https://news.ycombinator.com/item?id=45786738
  - community evidence that IDE selection shortcuts such as Cmd-L are a real
    ergonomic contrast against CLI-agent prompting.

The top positioning anchors remain:

1. VS Code / GitHub Copilot terminalSelection and Add Terminal Selection to Chat
2. iTerm2 AI Chat / Explain Output with AI
3. Cursor Agent terminal Add to Chat

Warp now appears explicitly in the A-layer close-adjacent set through blocks as
context and conversation forking, but it is not treated as a direct match
because it is Warp's own agent/terminal surface rather than an iTerm2 layer that
injects into an existing Claude Code/Codex/Aider/Gemini session.

## iTerm2 Feasibility Check

Local iTerm2 state:

```text
bundle id: com.googlecode.iterm2
installed app: /Applications/iTerm.app
current iTerm2 windows before/after disposable attempts: 6
current-session metadata readable by AppleScript:
  session.path
  id
  tty
```

AppleScript dictionary confirms these relevant primitives:

- `current session`
- `text` / visible contents
- `variable named ...`
- `write ... text ... newline false`

Disposable window creation through AppleScript returned `missing value` in this
Codex shell context, so no prompt-injection attempt was made against existing
user sessions.

More importantly, the machine already contains an external AgentUX prototype:

```text
<external-agentux-repo>
~/Library/Application Support/iTerm2/Scripts/AutoLaunch/agentux_iterm2.py
```

The installed iTerm2 AutoLaunch script points to that repo and already contains
selection-aware mechanics:

- `async_get_selection()` and `async_get_selection_text(...)`;
- Add, Explain, Review, Fix, Side, Branch actions;
- context-menu registrations such as `AgentUX Add to Conversation`;
- coding-agent detection for `codex`, `claude`, `aider`, and `gemini`;
- bracketed paste insertion with `suppress_broadcast=True`;
- success message states that inserted prompts are not submitted;
- collection basket for selections gathered outside coding-agent sessions;
- Branch, Project Branch, and Worktree Branch flows with prompt files and git
  metadata.

Project-scout should not absorb that implementation. The correct next step is
to review and verify the external AgentUX repo directly if AgentUX itself is the
active product.

## Completion Judgment

The remaining project-scout follow-up work is closed enough for this repo:

- focused GitHub/community follow-up was run through `project-scout`;
- web coverage was added as a curated candidate source;
- Warp blocks/context/forking were verified against primary docs;
- iTerm2 Add-mechanics feasibility was checked locally without mutating user
  terminal sessions;
- a stronger external AgentUX implementation was discovered and should be
  handled in its own repo.

Do not turn project-scout into an AgentUX implementation repo. Keep
project-scout as the scout/skill/reporting layer.
