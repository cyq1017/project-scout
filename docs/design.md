# project-scout Design

## Goal

`project-scout` helps a team look for similar projects before committing to a new project, major rebuild, or roadmap change. It produces evidence for build, adopt, fork, integrate, plugin, or compete decisions without making an irreversible decision for the user.

## MVP Architecture

The MVP is a Python package with a thin CLI. Core behavior lives in library modules so later wrappers can call the same functions from a Codex/Claude skill or a Conductor plugin.

```text
CLI -> brief parser -> candidate importer/search adapter -> scorer -> report writer
```

The default path is deterministic and local-first. Fixture and manual JSON imports are first-class so tests and repeatable research can run without network access. GitHub unauthenticated REST search is an adapter, not a required test dependency.

## Data Model

The brief captures:

- project name
- goal
- keywords
- target users
- technical stack
- exclusions

Candidates capture:

- name
- URL
- stars
- last update
- description
- topics
- license
- language
- README summary

Reports contain ranked candidates, an overlap matrix, recommendation evidence, risks, and suggested ADR/backlog updates.

## Scoring

Similarity is deterministic. The MVP combines keyword, stack, audience, topic, language, description, and README overlap. Exclusions reduce score and are also shown as risks or avoid signals.

Recommendations are evidence-based:

- `Borrow`: useful implementation ideas, little direct adoption fit.
- `Avoid`: clear mismatch, stale status, or excluded direction.
- `Integrate`: useful as dependency/service/tool.
- `Compete`: similar problem and audience, but differentiated enough to build.
- `Fork`: strong fit, compatible license, and likely lower cost than greenfield.
- `Ignore`: low overlap or insufficient evidence.

## Error Handling

The CLI should fail fast on malformed briefs, unreadable candidate files, invalid JSON, or unavailable output directories. Live GitHub failures should produce a clear error without writing partial reports.

## Testing

Tests use fixtures for briefs and candidate repositories. The CLI must be able to generate a sample report from fixtures without network access.
