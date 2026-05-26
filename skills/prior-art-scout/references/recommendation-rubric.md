# Recommendation Rubric

Use one shared vocabulary across projects, skills, plugins, tools, products, papers, and internal assets.

| Recommendation | Use when |
| --- | --- |
| `Adopt` | Existing solution satisfies the main need with acceptable license, cost, maintenance, and integration risk. |
| `Borrow` | Existing solution is not directly adoptable, but has useful UX, architecture, workflow, schema, prompts, or operating model. |
| `Integrate` | Existing solution should be connected as dependency, service, plugin, adapter, MCP server, or workflow step. |
| `Fork` | Existing implementation is close, source is available, license permits derivatives, and maintaining a fork is cheaper than greenfield. |
| `Extend` | Existing skill/plugin/tool is close but needs a wrapper, adapter, focused feature, localization, or target-specific workflow. |
| `Write New` | Existing solutions miss the core requirement or create unacceptable coupling, privacy, license, cost, or product risk. |
| `Avoid` | Candidate conflicts with exclusions, is stale or risky, has incompatible license, or solves a misleadingly similar but wrong problem. |
| `Ignore` | Low relevance or insufficient overlap. |
| `Monitor` | Promising but not actionable now due to maturity, missing docs, unstable ecosystem, or unclear fit. |

## Confidence

Decision confidence and coverage confidence are separate.

Decision confidence asks: "How strongly does the evidence support this recommendation?"

Coverage confidence asks: "How complete and well-distributed was the search?"

Never use high decision confidence when coverage confidence is low.
