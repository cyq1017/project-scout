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
        f"# {_inline_text(report.brief.name)} Prior-Art Map",
        "",
        f"Generated: {report.generated_at}",
        "",
        "## Executive Summary",
        "",
        (
            f"Reviewed {report.summary.candidate_count} candidate projects. "
            f"Top recommendation signal: **{report.summary.top_recommendation}**. "
            f"Decision confidence: **{report.decision.confidence}**. "
            f"Coverage confidence: **{report.coverage.confidence}**."
        ),
        "",
        "## Search Summary",
        "",
        "| Source | Query | Results | Used | Status | Notes |",
        "| --- | --- | ---: | ---: | --- | --- |",
    ]
    for entry in report.search_log:
        lines.append(
            "| "
            f"{_table_cell(entry.source)} | {_table_cell(entry.query)} | {entry.result_count} | {entry.used_count} | "
            f"{_table_cell(entry.status)} | {_table_cell(entry.error or '')} |"
        )
    lines.extend(
        [
            "",
            "## Source Requirements",
            "",
            "| Source | Required |",
            "| --- | --- |",
        ]
    )
    for source in report.coverage.source_requirements:
        lines.append(
            "| "
            f"{_table_cell(source['source'])} | {_table_cell('yes' if source['required'] else 'no')} |"
        )
    lines.extend(
        [
            "",
            "## Coverage Matrix",
            "",
            "| Source | Status | Used | Notes |",
            "| --- | --- | ---: | --- |",
        ]
    )
    for source in report.coverage.sources:
        lines.append(
            "| "
            f"{_table_cell(source['source'])} | {_table_cell(source['status'])} | {source['used_count']} | "
            f"{_table_cell(source.get('error') or '')} |"
        )
    lines.extend(
        [
            "",
            "## Similar Projects",
            "",
            "| Project | Kind | Stars | Updated | License | Language | Score | Recommendation |",
            "| --- | --- | ---: | --- | --- | --- | ---: | --- |",
        ]
    )
    for candidate in report.candidates:
        lines.append(
            "| "
            f"[{_link_text(candidate.name)}]({_link_url(candidate.url)}) | {_table_cell(candidate.kind)} | {candidate.stars} | "
            f"{_table_cell(candidate.last_update or 'unknown')} | {_table_cell(candidate.license or 'unknown')} | "
            f"{_table_cell(candidate.language or 'unknown')} | {candidate.similarity_score:.3f} | "
            f"{_table_cell(candidate.recommendation)} |"
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
            f"{_table_cell(row['candidate'])} | {row['keyword_overlap']} | {row['stack_overlap']} | "
            f"{row['user_overlap']} | {row['exclusion_overlap']} | {row['score']:.3f} |"
        )
    lines.extend(["", "## What To Borrow", ""])
    lines.extend(_borrow_lines(report))
    lines.extend(["", "## What To Avoid", ""])
    lines.extend(_avoid_lines(report))
    lines.extend(["", "## Recommendation And Confidence", ""])
    lines.extend(_recommendation_lines(report))
    lines.extend(["", "## Coverage Confidence And Blind Spots", ""])
    lines.extend(_coverage_lines(report))
    lines.extend(["", "## Differentiation Is Not Enough: Useful Positioning", ""])
    lines.extend(_positioning_lines(report))
    lines.extend(["", "## Risks And Unknowns", ""])
    lines.extend([f"- {_inline_text(risk)}" for risk in report.risks])
    lines.extend(["", "## Suggested ADR / Backlog Updates", ""])
    lines.extend([f"- {_inline_text(update)}" for update in report.suggested_updates])
    lines.append("")
    return "\n".join(lines)


def _borrow_lines(report: ScoutReport) -> list[str]:
    rows = []
    for candidate in report.candidates:
        if candidate.recommendation in {"Adopt", "Borrow", "Integrate", "Fork", "Extend"}:
            evidence = ", ".join(candidate.evidence) if candidate.evidence else "review implementation details"
            rows.append(f"- {_inline_text(candidate.name)}: borrow evidence around {_inline_text(evidence)}.")
    return rows or ["- No strong borrow signals found."]


def _avoid_lines(report: ScoutReport) -> list[str]:
    rows = []
    for candidate in report.candidates:
        if candidate.avoid_reasons:
            rows.append(f"- {_inline_text(candidate.name)}: {_inline_text('; '.join(candidate.avoid_reasons))}.")
        elif candidate.recommendation == "Ignore":
            rows.append(f"- {_inline_text(candidate.name)}: low overlap in available metadata.")
    return rows or ["- No explicit avoid signals found in the available metadata."]


def _recommendation_lines(report: ScoutReport) -> list[str]:
    lines = [
        f"- Recommendation: **{_inline_text(report.decision.recommendation)}**.",
        f"- Decision confidence: **{_inline_text(report.decision.confidence)}**.",
    ]
    lines.extend([f"- Rationale: {_inline_text(item)}" for item in report.decision.rationale])
    lines.extend([f"- Confidence reason: {_inline_text(item)}" for item in report.decision.confidence_reasons])
    lines.append("- Treat this as research input, not an automatic decision.")
    return lines


def _coverage_lines(report: ScoutReport) -> list[str]:
    lines = [
        f"- Coverage confidence: **{_inline_text(report.coverage.confidence)}**.",
        f"- Stop reason: {_inline_text(report.coverage.stop_reason)}",
    ]
    lines.extend([f"- Blind spot: {_inline_text(item)}" for item in report.coverage.blind_spots])
    return lines


def _positioning_lines(report: ScoutReport) -> list[str]:
    top_candidates = [candidate.name for candidate in report.candidates[:3]]
    if not top_candidates:
        return ["- Positioning is unknown until comparable projects are reviewed."]
    return [
        (
            "- Position around the workflow decision this tool enables: evidence-backed "
            "build/adopt/fork/plugin choices before roadmap commitment."
        ),
        f"- Compare explicitly against: {_inline_text(', '.join(top_candidates))}.",
    ]


def _inline_text(value: object) -> str:
    return " ".join(str(value).split())


def _table_cell(value: object) -> str:
    return _inline_text(value).replace("\\", "\\\\").replace("|", "\\|")


def _link_text(value: object) -> str:
    return _table_cell(value).replace("[", "\\[").replace("]", "\\]")


def _link_url(value: object) -> str:
    text = _inline_text(value)
    return text.replace(" ", "%20").replace("(", "%28").replace(")", "%29")
