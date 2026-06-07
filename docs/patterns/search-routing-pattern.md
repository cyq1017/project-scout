# Search Routing Pattern

## Problem

Discovery tasks often fail because the agent treats search as one generic tool.
Prior-art, competitive research, skill discovery, product research, and business
opportunity discovery need different source routes and confidence rules.

## Use When

Use this pattern when a skill or project needs to answer:

- Does this already exist?
- What alternatives or adjacent implementations exist?
- What should we adopt, borrow, fork, integrate, extend, or write new?
- How confident are we that the search covered the right source classes?

## Pattern

Separate the search stack into three layers:

| Layer | Role | Examples |
| --- | --- | --- |
| Protocol | Defines coverage, evidence, comparison, and recommendation | `prior-art-scout` |
| Adapters | Execute source access through available tools | WebSearch, GitHub CLI/API, skills registry, Jina, browser/CDP |
| Source patterns | Preserve platform-specific facts and pitfalls | GitHub query syntax, skills registry output, dynamic web pages |

The protocol must not depend on one adapter. An adapter can fail, be unavailable,
or require user approval; the protocol should record that as a coverage fact.

## Tool Escalation

Start with the lowest-permission route that can answer the question:

| Need | Default Route | Escalate When |
| --- | --- | --- |
| Find public candidates | Search engine, GitHub, skills registry | Search results are too noisy or source-specific search is needed |
| Read known URL | WebFetch, Jina, curl | Static extraction fails or page is dynamic |
| Inspect dynamic page | Browser automation | The page requires interaction, rendering, or session state |
| Use logged-in state | User browser/CDP | User explicitly asks and the task cannot be done publicly |
| Platform automation | Avoid by default | User explicitly accepts account/platform risk |

## Evidence Rules

- Search engines discover sources; they do not prove claims.
- Prefer primary sources for metadata and capability claims.
- Record source, query, result count, used count, status, and notes.
- State blind spots instead of implying exhaustive coverage.
- Run at least one query-expansion or snowball round for formal gates.

## Anti-pattern

- Binding a discovery skill to one search tool.
- Treating browser/CDP as the default path for public information.
- Treating install counts, stars, or SEO rank as proof of fitness.
- Saving raw dumps by default when summarized search logs are enough.

## Transfer

Use this pattern for future skills such as:

- business-opportunity discovery
- market research
- skill/plugin discovery
- paper/code prior-art discovery
- product alternatives research
- internal tool reuse gates

## Source

Derived from `prior-art-scout` development and Web Access analysis.

## Last Verified

2026-05-27
