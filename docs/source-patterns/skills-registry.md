# Skills Registry Source Pattern

## Use When

Use skills registry search when the target might already exist as an agent
skill, Claude/Codex skill, prompt workflow, or reusable agent capability.

## Routes

| Need | Preferred Route |
| --- | --- |
| Search by concept | `npx --yes skills find "<query>"` |
| Inspect listing | skills registry URL |
| Fallback | GitHub search with `skill`, `SKILL.md`, or registry-specific terms |

## Metadata To Capture

- skill name
- registry URL
- install count when available
- source repository if available
- declared trigger/description
- bundled references/scripts/assets
- agent compatibility claims

## Pitfalls

- Install count is weak evidence; it does not prove fit or quality.
- Registry output can include ANSI color codes and abbreviated counts.
- Some skills are wrappers around broader tools and require source inspection.

## Last Verified

2026-05-27
