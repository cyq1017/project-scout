# Skills Registry Source Pattern

## Use When

Use skills registry search when the target might already exist as an agent
skill, Claude/Codex skill, prompt workflow, or reusable agent capability.

## Routes

| Need | Preferred Route |
| --- | --- |
| Search by concept | `npx --yes skills find "<query>"` or `project-scout --skills-query "<query>" --skills-timeout <seconds>` |
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
- `npx --yes skills find` is a live command execution boundary. Keep it
  explicit, bounded, and recorded in the source log.
- Missing `npx`, timeouts, non-zero exits, and registry unavailability should be
  recorded as failed source entries; use GitHub/web fallback terms instead of
  treating the registry as covered.

## Last Verified

2026-06-20
