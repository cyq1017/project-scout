# BACKLOG

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
- Harden `prior-art-scout` skill against real quick-scan and formal-gate tasks.
- Add optional web search adapter.
- Add source-pattern docs for social, papers, packages, and job-market signals.
- Add optional LLM summarization adapter.
- Add user-level Codex/Claude skill install command.
- Add Conductor plugin/adapter boundary.
- Add configurable scoring weights.
- Add richer license and activity risk analysis.
- Add README language/section-aware summarization.

## Non-Goals

- No autonomous agent mode in MVP.
- No crawler platform.
- No token persistence.
- No automatic user-facing decisions.
- No issue, PR, or roadmap mutation.
