# Technical Due-Diligence Gate

Use this reference for Formal Gate runs and for any request that asks whether a
direction is worth building or adopting.

## Definition

Technical due diligence means evidence-backed review of existing solutions,
source coverage, candidate fit, integration risk, and build-vs-adopt options.
For this skill, it is a bounded technical evidence gate powered by recorded
sources and the `project-scout` report contract.

This skill does not perform legal, financial, acquisition, compliance, or
exhaustive market diligence. When those domains matter, state that the technical
report is only one input to a separate expert review.

## Claim Scope

Use this claim-scope language in Formal Gate artifacts:

```text
No exhaustive-search claim is made. Conclusions apply only to the recorded
sources, queries, dates, access constraints, and verification steps.
```

Do not turn "not found in recorded sources" into "does not exist".

## Quick Scan Exit Criteria

Quick Scan may stop when:

- the target and likely category are clear;
- at least the highest-value source class was checked or marked unavailable;
- user-provided known candidates were considered first;
- a compact candidate table or absence note is provided;
- uncertainty and the next source to check are stated.

Quick Scan should not write files by default and should not claim coverage is
complete.

## Formal Gate Exit Criteria

Formal Gate may stop when these artifacts or explicit gaps exist:

- Discovery Brief;
- source log;
- query matrix or query family notes;
- structured candidates;
- `project-scout` JSON report;
- Markdown report;
- coverage confidence;
- decision dashboard;
- blind spots;
- next validation steps.

If the `project-scout` engine is unavailable, produce a provisional Markdown and
JSON report using `report-contract.md`, record the missing engine as a process
gap, and keep decision confidence conservative.

## Decision Boundary

Formal Gate can recommend `Adopt`, `Borrow`, `Integrate`, `Fork`, `Extend`,
`Write New`, `Avoid`, `Ignore`, `Monitor`, or `Research More`, but the user owns
the final decision. The skill must not mutate issues, PRs, ADRs, roadmap, or
backlog unless the user explicitly asks.

## Evidence Thresholds

- `Research More`: required when source coverage is low, adapter failures hide
  important sources, or candidate evidence is too incomplete.
- `Write New`: report-level only, never a candidate label.
- `Adopt` or `Integrate`: require primary-source evidence for fit, license or
  terms, maintenance, integration boundary, and material risk categories.
- `Borrow`: allowed with partial evidence if the borrowed lesson is clearly
  separated from adoption.

## Completion Check

Before finalizing, verify:

- source failures are visible;
- coverage confidence is not stronger than the recorded sources justify;
- decision confidence is not stronger than coverage and evidence justify;
- top candidates include unknowns and risks;
- positioning claims avoid uniqueness unless primary evidence supports them.
