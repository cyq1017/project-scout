# Coverage Protocol

Do not claim exhaustive search. Claim defensible coverage.

## Coverage Matrix

For Formal Gate, create a coverage matrix before searching:

| Source | Status | Required? | Notes |
| --- | --- | --- | --- |
| GitHub | searched/skipped/rate_limited | yes/no | repo and code discovery |
| Skills registry | searched/skipped | yes/no | agent skill discovery |
| Manual candidates | included/none | yes | user-provided candidates |
| Web/product pages | searched/skipped | yes/no | product or SaaS discovery |
| Package registries | searched/skipped | yes/no | library/tool discovery |
| Papers | searched/skipped | yes/no | research discovery |
| Internal assets | searched/skipped/user_declined | yes/no | only when user provides paths |

Every skipped or unavailable source needs a reason.

## Query Expansion

Search beyond the user's exact wording:

- name variants
- synonyms
- ecosystem terms
- shape terms such as `skill`, `plugin`, `MCP`, `desktop`, `CLI`, `agent`, `library`, `SaaS`
- decision terms such as `alternative`, `competitor`, `build vs buy`, `build vs adopt`, `open source`

Record representative queries in the search log.

## Snowball Search

After finding candidates, inspect them for:

- README links
- related projects
- docs integrations
- GitHub topics
- package names
- "alternatives" and "compare" pages
- community mentions

Run at least one additional query round when strong candidates reveal new terms.

## Negative Search

Search for mismatch and alternatives:

- `X alternative`
- `X vs Y`
- `open source alternative to X`
- `why not use X`
- `X competitor`
- `X plugin`
- `X skill`

This finds candidates that do not appear in direct positive queries.

## Stop Criteria

Formal Gate may stop when:

- required sources are searched or explicitly marked unavailable
- user-provided known candidates are included
- at least two query rounds produce no new high-overlap candidates, or remaining new candidates are low-signal duplicates
- recommendation confidence and coverage confidence are explainable
- blind spots are listed

## Coverage Confidence

Use `Low`, `Medium`, or `High`.

- `High`: required sources covered, query expansion and snowball search completed, metadata verified from primary sources.
- `Medium`: major sources covered, but some metadata or source classes remain incomplete.
- `Low`: source access is limited, candidate set is mostly manual, or search was blocked by rate limits.

Always include known blind spots. This is more credible than pretending the search is complete.
