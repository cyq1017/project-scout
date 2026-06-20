# Query Matrix

Use this reference to turn a discovery brief into concrete search queries before
running source adapters or the `project-scout` engine.

## Query Families

Build a matrix from the target definition:

| Family | Purpose | Examples |
| --- | --- | --- |
| Name | Find exact known candidates and official pages | `AgentUX`, `"AgentUX" terminal` |
| Synonym | Catch different wording for the same job | `terminal selection assistant`, `selected terminal text AI` |
| Ecosystem | Search where the target would naturally live | `iTerm2 Python API`, `tmux copy mode`, `VS Code terminal selection` |
| Shape | Search by implementation form | `plugin`, `skill`, `MCP server`, `CLI`, `desktop app`, `overlay` |
| Problem | Search the user pain or workflow | `add selected terminal output to chat`, `ask AI about terminal output` |
| Competitor | Search alternatives and comparison pages | `alternative`, `competitor`, `vs`, `open source alternative` |
| Negative | Search mismatch and reasons not to build | `generic AI terminal`, `command generator only`, `why not use` |
| Community | Search discussion and adoption signals | `Reddit`, `Hacker News`, `forum`, `issue`, `discussion` |

## Target Examples

| Target type | Query emphasis |
| --- | --- |
| `skill` | skill name, `SKILL.md`, registry name, workflow terms, trigger terms |
| `plugin` | host product, extension API, marketplace, integration boundary |
| `product` | official docs, alternatives, reviews, comparison pages, pricing/security docs |
| `mcp_server` | exposed tools, transport, auth model, client compatibility |
| `paper` | method terms, benchmark terms, code links, citations, prior work |
| `market_opportunity` | user pain, jobs-to-be-done, community complaints, existing products |

## Quality Gates

- Search known candidates directly before broad queries.
- For Quick Scan, run at least one synonym or shape expansion unless the answer
  is already blocked by user-provided evidence.
- For Formal Gate, run at least two rounds: direct/synonym queries, then
  snowball or negative queries based on discovered candidates.
- Record source, query, result count, used count, status, and notes in the
  source log or report inputs.
- Treat unavailable sources as blind spots, not evidence that the target has no
  prior art.
- Feed normalized candidates into `project-scout`; do not hand-write
  deterministic scoring when the engine is available.

## Stop Rule

Stop when required sources are searched or marked unavailable, known candidates
are represented or recorded as missing, and the remaining new results are
duplicates or low-signal broad-adjacent candidates.
