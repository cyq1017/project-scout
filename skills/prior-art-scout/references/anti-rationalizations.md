# Anti-Rationalizations

Use this reference when the agent starts to compress evidence, skip a source, or
turn weak coverage into a strong conclusion. The required response should be
reflected in the `project-scout` search log, coverage, blind spots, or final
discussion.

| Rationalization | Why it is wrong | Required response |
| --- | --- | --- |
| No results means no competitors | Search coverage is bounded and source-dependent. | Record the source/query scope, add a blind spot, and prefer `Research More` unless coverage is strong. |
| Stars prove adoption | Stars are popularity hints, not fit, license, maintenance, cost, security, or integration evidence. | Treat stars as community signal only and verify primary evidence. |
| LLM summary replaces primary source | Summaries can omit constraints, terms, and mismatch details. | Use summaries only as triage; cite primary sources for adoption claims. |
| One high-score candidate means Adopt | Relevance score is not adoption readiness. | Check license, maintenance, integration, cost, and security evidence before adoption language. |
| Coverage low but recommendation high | Decision confidence must not outrun source coverage. | Downgrade confidence and explain missing sources. |
| Write New from one weak candidate | `Write New` is report-level and depends on the whole candidate set and coverage. | Label weak candidates as `Ignore`, `Avoid`, or `Monitor`; reserve `Write New` for the report decision. |
| A web result can stand in for manual known-candidate coverage | Source classes carry different evidence quality and recall meaning. | Include manual known candidates separately or mark the source requirement missing. |
| A failed adapter can be ignored if another source worked | Failed adapters are coverage facts, not implementation noise. | Record failed source status, error, and fallback path. |
| A direct name match proves similarity | Names can collide across domains and workflows. | Inspect workflow, users, integration, and must-have fit. |
| Community buzz proves product fit | Community mentions are adoption signals, not requirements evidence. | Use community data as supporting context only. |
| The final answer can omit blind spots because it sounds less confident | Blind spots are part of the evidence contract. | Include material blind spots in the summary. |

## Minimum Enforcement

If any rationalization appears during a Formal Gate, the final answer must show
one of these corrections:

- a lower coverage or decision confidence;
- a `Research More`, `Monitor`, `Borrow`, or manual-review recommendation;
- a recorded blind spot;
- a next validation step tied to the missing evidence.

## project-scout Boundary

Use `project-scout` to make these corrections visible in the JSON and Markdown
reports when possible. If the engine is unavailable, record the same correction
in the provisional source log and discussion.
