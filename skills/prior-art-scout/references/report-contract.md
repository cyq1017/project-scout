# Report Contract

Formal Gate must write a human Markdown report and a machine JSON report.

## Markdown Sections

Required:

1. Executive Summary
2. Positioning Brief
3. Decision Dashboard
4. Search Summary
5. Source Requirements
6. Coverage Matrix
7. Similar Projects
8. Overlap Matrix
9. What To Borrow
10. What To Avoid
11. Recommendation And Confidence
12. Coverage Confidence And Blind Spots
13. Differentiation Map
14. Differentiation Is Not Enough: Useful Positioning
15. Risks And Unknowns
16. Suggested ADR / Backlog Updates

## JSON Fields

Recommended top-level shape:

```json
{
  "brief": {},
  "generated_at": "",
  "mode": "formal_gate",
  "summary": {},
  "decision": {
    "recommendation": "Borrow",
    "confidence": "Medium",
    "rationale": [],
    "confidence_reasons": []
  },
  "decision_dashboard": {
    "status": "ready_for_manual_review",
    "go_no_go": "review",
    "primary_action": "",
    "review_queue": [],
    "open_questions": []
  },
  "coverage": {
    "confidence": "Medium",
    "sources": [],
    "blind_spots": [],
    "stop_reason": ""
  },
  "search_log": [],
  "candidates": [],
  "overlap_matrix": [],
  "recommendations": [],
  "risks": [],
  "suggested_updates": []
}
```

Search log entries should be structured:

```json
{
  "source": "github|skills|web|manual|internal",
  "query": "",
  "result_count": 0,
  "used_count": 0,
  "status": "ok|empty|rate_limited|failed",
  "error": null
}
```

Do not store raw result dumps by default. Save raw dumps only when the user explicitly requests a complete audit trail.
