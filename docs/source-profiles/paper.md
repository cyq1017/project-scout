# Source Profile: Paper

## Use When

Use this profile when comparing a research direction, algorithm, benchmark, or
paper-backed implementation before adoption.

## Required Sources

| Source | Required? | Reason |
| --- | --- | --- |
| Papers | yes | Captures the primary claim and method lineage. |
| GitHub | yes | Finds reference implementations and reproducibility signals. |
| Package registries | optional | Useful when the method is packaged as a library. |
| Web/project pages | optional | Useful for demos, datasets, and leaderboard context. |
| Community sources | optional | Useful for replication reports and caveats. |

## Query Seeds

- paper title
- method name + "github"
- benchmark name + method name
- author name + implementation
- method name + "reproduction"

## Stop Criteria

- The primary paper, at least one implementation, and any known benchmark claim
  are represented or named as unavailable.
- The report separates paper claims from implementation maturity.
- Known datasets or benchmark dependencies are captured as risks.

## Blind Spots To Name

- Benchmark claims may not reproduce in local settings.
- Implementations can lag paper revisions.
- Licensing or dataset terms may block adoption.
