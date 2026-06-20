# Skill Repository Strategy

`project-scout` is evolving into a personal and public skill research repository. The CLI/library remains the deterministic engine. Skills wrap that engine and add agent workflow judgment.

## Layers

1. **Engine**
   - Python package under `src/project_scout`.
   - Deterministic parsing, scoring, normalization, and report generation.
   - Testable without live network access.

2. **Skill Source**
   - Skill folders under `skills/`.
   - `skills/prior-art-scout` is the first reusable skill.
   - The repo is the source of truth for skill development and public distribution.

3. **Installed Skill**
   - User-level copy or symlink under `~/.codex/skills` for daily use.
   - Installed version should be generated from repo source, not edited ad hoc.

4. **Adapters**
   - Web/search skills provide source access.
   - `find-skills` or skills registry search discovers existing skills.
   - `skill-creator` helps create or update skills.
   - `code-reviewer` and verification skills check implementation quality.

## How To Use Other Skills

Use other skills as composable capabilities:

- **Web Access / agent-reach**: source discovery and web reading.
- **find-skills**: search the skill ecosystem before writing a new skill.
- **skill-creator**: scaffold and validate skill folders.
- **code-reviewer**: review code changes after implementation.
- **verification-before-completion**: require fresh verification before claiming completion.

Do not merge all behavior into `prior-art-scout`. It should orchestrate discovery and reporting, while adjacent skills provide source access, creation, review, and verification.

## Skill Pack Strategy

`prior-art-scout` should remain the single public trigger skill until
forward-tests prove that separate triggers improve execution. Treat its
`references/` files as internal phase modules:

- source coverage and query planning;
- candidate evidence review;
- positioning and differentiation;
- build-vs-adopt decision gating;
- cross-agent execution;
- anti-rationalization and safety checks.

Do not split subskills only because the reference set is large. Split only when
a phase has a clear standalone trigger, needs its own scripts or assets, or two
forward-tests show agents skip the phase inside the parent skill. See
`skills/prior-art-scout/references/skill-pack-routing.md`.

Potential future subskills are:

- `source-coverage-scout`;
- `candidate-evidence-review`;
- `positioning-differentiator`;
- `build-vs-adopt-gate`.

Any future subskill that influences recommendations must state whether it uses
an existing `project-scout` report or is provisional.

## Community Packaging

For GitHub promotion, the repository should include:

- clear README with problem statement and examples
- `skills/prior-art-scout` source
- CLI usage examples
- sample reports
- safety policy
- contribution guidance for new source adapters and rubrics

Do not publish or push without explicit user approval.

## Local Install

Keep repo source and installed skill separate:

```bash
mkdir -p ~/.codex/skills
rm -rf ~/.codex/skills/prior-art-scout
cp -R skills/prior-art-scout ~/.codex/skills/prior-art-scout
```

Do not edit the installed copy directly. Make changes in `skills/prior-art-scout`, validate them, then reinstall.

Validation commands:

```bash
.venv/bin/python ${HOME}/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/prior-art-scout
.venv/bin/python -m pytest
```
