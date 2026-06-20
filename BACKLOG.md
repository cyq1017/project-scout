# BACKLOG

## Milestones

- [x] M1: Local prior-art gate. See `docs/milestones/m1-local-prior-art-gate.md`.
- [x] M2: Skill quality gate. See `docs/milestones/m2-skill-quality-gate.md` and `docs/plans/2026-06-20-prior-art-scout-m2-skill-quality-plan.md`.
- [x] M2 local dogfood: AgentUX run recorded in `docs/case-studies/2026-06-agentux-skill-quality-dogfood.md`.
- [x] M2 fresh-agent review: Codex fresh-agent run recorded in `docs/research/2026-06-20-agentux-codex-fresh-agent-review.md`.

## MVP

- [x] Initialize standalone Python CLI/library project.
- [x] Document local-first prior-art discovery scope.
- [x] Parse project briefs with name, goal, keywords, target users, stack, and exclusions.
- [x] Import candidates from fixture/manual JSON.
- [x] Import candidates from newline-delimited manual URL lists.
- [x] Search GitHub repositories without login.
- [x] Normalize repository metadata.
- [x] Score deterministic similarity and overlap.
- [x] Recommend Adopt, Borrow, Integrate, Fork, Extend, Write New, Avoid, Ignore, or Monitor with evidence.
- [x] Emit Markdown and JSON reports.
- [x] Cover core behavior with fixture tests.
- [x] Add `prior-art-scout` skill source.
- [x] Add DiscoveryBrief compatibility mapping.
- [x] Add structured search log and coverage confidence.
- [x] Add coverage matrix and blind spots to Markdown.
- [x] Add skills registry parser and CLI adapter.
- [x] Add repo-level experience library for reusable skill/project lessons.
- [x] Add search adapter reference for capability-based source access.

## Next

- [x] Harden dev bootstrap and smoke scripts.
- [x] Document Python 3.14/macOS editable install issue.
- [x] Add pytest coverage for the installed console script.
- [ ] Consider moving the checkout outside iCloud if hidden/dataless venv flags recur.
- [x] Move tracked root `project-scout-report.json` into `examples/`.
- [x] Add reusable brief templates for common scout tasks.
- [x] Add multi-query GitHub scan.
- [x] Add source-profile presets for `market_opportunity`, `product`, `paper`, and `mcp_server`.
- [x] Harden `prior-art-scout` skill against real quick-scan and formal-gate tasks.
- [x] Add optional web search adapter.
- [x] Add source-pattern docs for social, papers, packages, and job-market signals.
- [x] Add optional LLM summarization adapter.
- [x] Add user-level Codex/Claude skill install command.
- [x] Add Conductor plugin/adapter boundary.
- [x] Add configurable scoring weights.
- [x] Add richer license and activity risk analysis.
- [x] Add README language/section-aware summarization.
- [x] Add trustworthiness hardening plan.
- [x] Make empty candidate sets produce partial `Research More` reports.
- [x] Keep `Write New` as a report-level decision rather than candidate disposition.
- [x] Cap decision confidence by coverage confidence.
- [x] Escape Markdown report table/list content.
- [x] Preserve `DiscoveryBrief` fields through scoring and source policy.
- [x] Replace source-name coverage heuristics with explicit source requirements.
- [x] Generalize repository-centric candidates for products, papers, skills, plugins, and MCP-style servers.
- [x] Add Unicode/CJK-aware relevance matching.
- [x] Add structured evidence records for license, maintenance, integration, pricing, and security.
- [x] Split report-level adoption readiness gates out of core orchestration.
- [x] Add deterministic differentiation map and README positioning draft.
- [x] Add first-page positioning brief with closest alternatives and candidate roles.
- [x] Add first-page decision dashboard with go/review/hold, review queue, and open questions.
- [ ] Investigate GitHub adapter DNS failures in Codex CLI shell runtime.
- [ ] Harden or document skills-registry timeout behavior for fresh-agent runs.
- [ ] Run a focused GitHub/community follow-up for AgentUX small-plugin prior art.
- [ ] Manually verify Warp blocks/context/forking behavior against AgentUX Add/Branch claims.

## Non-Goals

- No autonomous agent mode in MVP.
- No crawler platform.
- No token persistence.
- No automatic user-facing decisions.
- No issue, PR, or roadmap mutation.
