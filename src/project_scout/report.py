from __future__ import annotations

import json
from pathlib import Path

from project_scout.models import ScoutReport


def write_report(report: ScoutReport, *, out_json: str | Path, out_md: str | Path) -> None:
    json_path = Path(out_json)
    md_path = Path(out_md)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report.to_dict(), indent=2) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(report), encoding="utf-8")


def render_markdown(report: ScoutReport) -> str:
    lines = [
        f"# {report.brief.name} Prior-Art Map",
        "",
        f"Generated: {report.generated_at}",
        "",
        "## Executive Summary",
        "",
        (
            f"Reviewed {report.summary.candidate_count} candidate projects. "
            f"Top recommendation signal: **{report.summary.top_recommendation}**."
        ),
        "",
        "## Similar Projects",
        "",
        "| Project | Stars | Updated | License | Language | Score | Recommendation |",
        "| --- | ---: | --- | --- | --- | ---: | --- |",
    ]
    for candidate in report.candidates:
        lines.append(
            "| "
            f"[{candidate.name}]({candidate.url}) | {candidate.stars} | "
            f"{candidate.last_update or 'unknown'} | {candidate.license or 'unknown'} | "
            f"{candidate.language or 'unknown'} | {candidate.similarity_score:.3f} | "
            f"{candidate.recommendation} |"
        )
    lines.extend(
        [
            "",
            "## Overlap Matrix",
            "",
            "| Project | Keywords | Stack | Users | Exclusions | Score |",
            "| --- | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for row in report.overlap_matrix:
        lines.append(
            "| "
            f"{row['candidate']} | {row['keyword_overlap']} | {row['stack_overlap']} | "
            f"{row['user_overlap']} | {row['exclusion_overlap']} | {row['score']:.3f} |"
        )
    lines.extend(["", "## What To Borrow", ""])
    lines.extend(_borrow_lines(report))
    lines.extend(["", "## What To Avoid", ""])
    lines.extend(_avoid_lines(report))
    lines.extend(["", "## Build / Adopt / Fork / Plugin Recommendation", ""])
    lines.extend(_recommendation_lines(report))
    lines.extend(["", "## Differentiation Is Not Enough: Useful Positioning", ""])
    lines.extend(_positioning_lines(report))
    lines.extend(["", "## Risks And Unknowns", ""])
    lines.extend([f"- {risk}" for risk in report.risks])
    lines.extend(["", "## Suggested ADR / Backlog Updates", ""])
    lines.extend([f"- {update}" for update in report.suggested_updates])
    lines.append("")
    return "\n".join(lines)


def _borrow_lines(report: ScoutReport) -> list[str]:
    rows = []
    for candidate in report.candidates:
        if candidate.recommendation in {"Borrow", "Integrate", "Fork", "Compete"}:
            evidence = ", ".join(candidate.evidence) if candidate.evidence else "review implementation details"
            rows.append(f"- {candidate.name}: borrow evidence around {evidence}.")
    return rows or ["- No strong borrow signals found."]


def _avoid_lines(report: ScoutReport) -> list[str]:
    rows = []
    for candidate in report.candidates:
        if candidate.avoid_reasons:
            rows.append(f"- {candidate.name}: {'; '.join(candidate.avoid_reasons)}.")
        elif candidate.recommendation == "Ignore":
            rows.append(f"- {candidate.name}: low overlap in available metadata.")
    return rows or ["- No explicit avoid signals found in the available metadata."]


def _recommendation_lines(report: ScoutReport) -> list[str]:
    if not report.recommendations:
        return ["- Recommendation: gather candidates before making a build/adopt/fork/plugin call."]
    top = report.recommendations[0]
    evidence = ", ".join(top["evidence"]) if top["evidence"] else "limited metadata"
    return [
        (
            f"- Recommendation: **{top['recommendation']}** with `{top['candidate']}` "
            f"as the strongest current signal."
        ),
        f"- Evidence: {evidence}.",
        "- Treat this as research input, not an automatic decision.",
    ]


def _positioning_lines(report: ScoutReport) -> list[str]:
    top_candidates = [candidate.name for candidate in report.candidates[:3]]
    if not top_candidates:
        return ["- Positioning is unknown until comparable projects are reviewed."]
    return [
        (
            "- Position around the workflow decision this tool enables: evidence-backed "
            "build/adopt/fork/plugin choices before roadmap commitment."
        ),
        f"- Compare explicitly against: {', '.join(top_candidates)}.",
    ]
