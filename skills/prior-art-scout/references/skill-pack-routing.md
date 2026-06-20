# Skill Pack Routing

Use this reference when deciding whether `prior-art-scout` should remain one
skill with references or split into multiple independently triggered skills.

## Current M4 Decision

Keep one public trigger skill for now:

```text
prior-art-scout
```

Use references as internal phase modules:

- source coverage;
- candidate evidence review;
- positioning discussion;
- build-vs-adopt decision gate;
- cross-agent execution;
- safety and anti-rationalizations.

This keeps evidence continuity intact: the same run defines the brief, searches
sources, records coverage, evaluates candidates, runs `project-scout`, and
interprets the decision.

## Future Optional Subskills

Create a subskill only when it has a clear standalone trigger and does not
weaken the evidence chain.

| Proposed subskill | Trigger | Owns | Should not own |
| --- | --- | --- | --- |
| `source-coverage-scout` | user asks only about search coverage or source gaps | sources, queries, source log, coverage matrix | final adoption decision |
| `candidate-evidence-review` | user asks whether candidates are trustworthy or adoption-ready | evidence quality, primary-source gaps, material risks | discovery breadth |
| `positioning-differentiator` | user asks what is unique, defensible, or worth saying in README | positioning, claims to avoid, borrow/compete guidance | source collection |
| `build-vs-adopt-gate` | user asks whether to build, adopt, integrate, fork, extend, or borrow | decision gate, confidence, next validation | raw search |

## Split Criteria

Split a phase into a real subskill only when at least one of these is true:

- two forward-tests show agents skip that phase in the parent skill;
- users ask for that phase as a standalone task three or more times;
- the phase needs its own scripts, assets, or validation flow;
- the subskill trigger is clearer than the parent skill trigger;
- the phase is useful outside prior-art reports.

## Do-Not-Split Criteria

Do not create a subskill when:

- the motivation is only aesthetics;
- the reason is only that there are many references;
- splitting makes agents skip `project-scout` engine output;
- splitting separates evidence review from source coverage;
- the child skill would mostly repeat parent instructions.

## Routing Rules

- Use `prior-art-scout` for full Quick Scan and Formal Gate work.
- Use future subskills only for scoped follow-up tasks after a source log or
  candidate set already exists.
- When in doubt, keep the parent skill in charge and load the relevant
  reference.

## project-scout Boundary

Any future subskill that produces recommendations must state whether it relies
on an existing `project-scout` report or is provisional. Only the parent skill
should own end-to-end Formal Gate completion until forward-tests justify a
different split.
