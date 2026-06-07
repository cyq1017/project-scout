# Skill Experience Library

## Purpose

Use this repo-level library to preserve reusable lessons from building, testing,
shipping, and promoting skills. Keep finished skills lean; keep accumulated
design knowledge here.

## Repository Roles

| Area | Role | Belongs Here |
| --- | --- | --- |
| `skills/` | Installable skill source | Runtime instructions, references, scripts, assets needed by agents |
| `docs/patterns/` | Reusable methods | General design patterns that can transfer to future skills or projects |
| `docs/case-studies/` | Evidence-rich examples | What we inspected, learned, borrowed, avoided, or changed |
| `docs/templates/` | Repeatable forms | Briefs, checklists, matrices, report shells |
| `docs/source-patterns/` | Source-specific search notes | Platform behavior, useful queries, pitfalls, fallback routes |
| `DEVLOG.md` | Chronological work log | What changed and why, in brief |
| `HANDOFF.md` | Continuity state | Current state, verification, known gotchas |

## Experience Promotion Flow

```text
conversation or experiment
  -> DEVLOG factual note
  -> case study when there is enough evidence
  -> pattern when it generalizes
  -> template/checklist when it should be repeated
  -> skill reference only when agents need it during execution
```

## Promotion Criteria

Move an observation into a skill reference only when all are true:

- It directly changes how the agent should perform the task.
- It reduces repeated mistakes, missed sources, or unsafe behavior.
- It is independent of the current conversation.
- It is concise enough to justify context cost.
- It does not duplicate repo-level design history.

Otherwise keep it in `docs/`.

## Experience Card Format

```markdown
# Pattern Name

## Problem

The recurring problem or decision pressure.

## Use When

When the pattern applies.

## Pattern

The recommended approach.

## Anti-pattern

What to avoid.

## Transfer

How to reuse it in future skills, plugins, or projects.

## Source

Where the lesson came from.

## Last Verified

YYYY-MM-DD
```

## Maintenance

- Prefer small, named documents over one large knowledge dump.
- Keep source-specific facts dated and easy to revise.
- Treat popularity, installs, stars, and SEO rank as weak evidence unless
  confirmed by primary sources or usage context.
- When a lesson becomes part of an installable skill, link back to the source
  case study instead of copying the whole analysis.
