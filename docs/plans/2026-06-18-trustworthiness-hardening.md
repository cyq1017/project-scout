# project-scout Trustworthiness Hardening

Status: Active
Baseline: `15575296d18cbee426c2b63836d2033a29e879c3`
Date: 2026-06-18

This plan narrows the larger architecture review into small, fixture-first
hardening work. The goal is to make reports less misleading when source
coverage is partial, candidate evidence is weak, or live adapters fail.

## Scope

- Keep `project-scout` local-first and fixture-first.
- Keep CLI behavior deterministic and auditable.
- Do not add a crawler, login flow, token storage, or LLM-only scoring.
- Do not replace the current model layer with a full v2 schema in this slice.

## Current Slice

- Candidate-level recommendations do not include `Write New`.
- `Write New` is reserved for report-level decisions when coverage is high and
  candidates are still too weak for adopt, integrate, fork, or borrow.
- Source failures and empty candidate sets produce partial reports with
  `Research More` instead of terminating the CLI.
- Decision confidence is capped by coverage confidence.
- Markdown report content is escaped before table/list rendering.
- Discovery briefs are preserved in report JSON and normalized only internally
  for scoring.
- Coverage reports target-specific source requirements and known-candidate
  misses.
- Candidate metadata supports `kind` and source-specific `attributes`.
- Relevance matching includes basic CJK lexical overlap.
- Scored candidates include structured evidence records for license,
  maintenance, primary-source URL, integration, and pricing/security.
- Report-level adoption readiness and candidate disposition gates are split into
  `project_scout.recommendation`.
- Reports include a deterministic differentiation map with commodity features,
  unique combination, claims to avoid, comparison guidance, and a conservative
  README positioning draft.
- Reports include a first-page positioning brief with verdict, closest
  alternatives, candidate roles, recommended positioning, and next validation
  steps.
- Reports include a first-page decision dashboard with go/review/hold, primary
  action, review queue, and open questions derived from coverage and evidence
  gaps.

## Later Slices

- Move relevance scoring into its own module if it grows beyond the current
  compact implementation.
