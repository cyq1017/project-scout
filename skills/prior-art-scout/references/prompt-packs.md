# Prompt Packs

Use these prompts when handing prior-art work to another agent or reviewer. Keep
the target text specific, keep artifacts under `/tmp` unless the user asks
otherwise, and preserve the project-scout boundary.

## Quick Scan Prompt

```text
Use prior-art-scout for a Quick Scan.

Target:
<one paragraph describing the idea, project, tool, skill, plugin, paper, or
product direction>

Must-have overlap:
- <requirement 1>
- <requirement 2>
- <requirement 3>

Known candidates:
- <candidate or none>

Instructions:
- Do not write files by default.
- Check bounded primary sources first.
- Separate direct, close adjacent, broad adjacent, and not relevant candidates.
- Do not claim exhaustive discovery.
- Return the verdict, closest candidates, why similar / different, uncertainty,
  and the next source to check.
```

## Formal Gate Prompt

```text
Use prior-art-scout for a Formal Gate technical due-diligence review.

Target:
<detailed target definition>

Decision question:
Should we build, adopt, integrate, fork, extend, borrow from, monitor, or
research more before committing roadmap work?

Scope:
- Target type: <project | skill | plugin | product | paper | mcp_server | market_opportunity>
- Must-have requirements: <list>
- Exclusions: <list>
- Known candidates: <list or none>

Instructions:
- Use the skill's source-routing, query-matrix, candidate-evidence, and
  anti-rationalization references.
- Use project-scout for deterministic scoring and report generation when
  available.
- Write draft artifacts under `/tmp`.
- Record source queries, errors, result counts, used counts, and blind spots.
- Do not claim exhaustive discovery.
- Do not operate external repositories; record external follow-ups only.
- Return artifact paths, recommendation, decision confidence, coverage
  confidence, go/review/hold status, comparison anchors, borrow/adopt/integrate
  signals, avoid/unknown signals, blind spots, and next validation.
```

## Reviewer Prompt

```text
Review the report artifacts from a prior-art-scout Formal Gate.

Artifacts:
- Markdown report: <path>
- JSON report: <path>
- Source log or query notes: <path>

Review focus:
- Are source log entries concrete and honest about failures?
- Are direct, close adjacent, broad adjacent, and not relevant candidates
  separated clearly?
- Does recommendation confidence stay capped by coverage and unknown evidence?
- Are comparison anchors supported by evidence instead of broad lexical matches?
- Are uniqueness, adoption, and Write New claims calibrated?
- Are external repositories treated only as evidence or follow-up, not operated?

Instructions:
- Review the report artifacts, not the target repo.
- Do not operate external repositories.
- List blocking evidence gaps first.
- Then list non-blocking improvements and final review verdict.
```
