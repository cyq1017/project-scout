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

## Later Slices

- Preserve `DiscoveryBrief` fields through scoring and source policy.
- Introduce a source requirement plan instead of inferring coverage from source
  names alone.
- Add explicit evidence records for license, maintenance, integration, pricing,
  security, and primary-source verification.
- Generalize repository-centric candidate metadata for products, papers, skills,
  plugins, and MCP-style servers.
- Add Unicode/CJK-aware relevance matching.
