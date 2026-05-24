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
- [x] Recommend Borrow, Avoid, Integrate, Compete, Fork, or Ignore with evidence.
- [x] Emit Markdown and JSON reports.
- [x] Cover core behavior with fixture tests.

## Next

- Add optional web search adapter.
- Add optional LLM summarization adapter.
- Add Codex/Claude skill wrapper.
- Add Conductor plugin/adapter boundary.
- Add configurable scoring weights.
- Add richer license and activity risk analysis.
- Add README fetching for GitHub search candidates when rate limits allow.

## Non-Goals

- No autonomous agent mode in MVP.
- No crawler platform.
- No token persistence.
- No automatic user-facing decisions.
- No issue, PR, or roadmap mutation.
