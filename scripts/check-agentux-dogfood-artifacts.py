#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


REQUIRED_FILES = [
    "agentux-brief.json",
    "agentux-candidates.json",
    "agentux-report.json",
    "agentux-prior-art-map.md",
    "agentux-source-log.md",
    "agentux-chat-summary.md",
]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check the local AgentUX prior-art-scout dogfood artifact bundle."
    )
    parser.add_argument(
        "--dir",
        default="/tmp",
        help="Directory containing agentux-* dogfood artifacts. Defaults to /tmp.",
    )
    args = parser.parse_args(argv)

    root = Path(args.dir)
    failures = check_bundle(root)
    if failures:
        print("FAIL AgentUX dogfood artifacts")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PASS AgentUX dogfood artifacts")
    for filename in REQUIRED_FILES:
        print(f"- {filename}")
    return 0


def check_bundle(root: Path) -> list[str]:
    failures: list[str] = []
    for filename in REQUIRED_FILES:
        if not (root / filename).exists():
            failures.append(f"missing {filename}")

    if failures:
        return failures

    brief = _read_json(root / "agentux-brief.json", failures)
    candidates = _read_json(root / "agentux-candidates.json", failures)
    report = _read_json(root / "agentux-report.json", failures)

    if isinstance(brief, dict):
        _check_brief(brief, failures)
    if isinstance(candidates, list):
        _check_candidates(candidates, failures)
    else:
        failures.append("agentux-candidates.json must contain a list")
    if isinstance(report, dict):
        _check_report(report, failures)

    _check_markdown(
        root / "agentux-prior-art-map.md",
        ["decision dashboard", "coverage confidence"],
        failures,
    )
    _check_markdown(
        root / "agentux-source-log.md",
        ["query matrix", "query"],
        failures,
    )
    _check_markdown(
        root / "agentux-chat-summary.md",
        [
            ["direct competitor"],
            ["coverage confidence"],
            ["claims to avoid", "should not claim", "unsupported uniqueness"],
            ["next validation"],
        ],
        failures,
    )
    return failures


def _read_json(path: Path, failures: list[str]) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        failures.append(f"{path.name} is invalid JSON: {error}")
    return None


def _check_brief(brief: dict[str, Any], failures: list[str]) -> None:
    text = " ".join(str(brief.get(key, "")) for key in ("name", "goal", "target_type"))
    if "agentux" not in text.lower():
        failures.append("agentux-brief.json must describe AgentUX")


def _check_candidates(candidates: list[Any], failures: list[str]) -> None:
    if not candidates:
        failures.append("agentux-candidates.json must include at least one candidate")
        return
    first_named = any(
        isinstance(candidate, dict) and (candidate.get("name") or candidate.get("title"))
        for candidate in candidates
    )
    if not first_named:
        failures.append("agentux-candidates.json candidates need name or title fields")


def _check_report(report: dict[str, Any], failures: list[str]) -> None:
    summary = _dict(report.get("summary"))
    decision = _dict(report.get("decision"))
    dashboard = _dict(report.get("decision_dashboard"))
    coverage = _dict(report.get("coverage"))
    differentiation = _dict(report.get("differentiation"))
    search_log = report.get("search_log")
    candidates = report.get("candidates")

    candidate_count = _positive_int(summary.get("candidate_count"))
    if candidate_count is None:
        failures.append("agentux-report.json summary.candidate_count must be an integer")
    elif candidate_count <= 0:
        failures.append("agentux-report.json summary.candidate_count must be greater than zero")
    if not decision.get("recommendation"):
        failures.append("agentux-report.json decision.recommendation is required")
    if decision.get("confidence") not in {"Low", "Medium", "High"}:
        failures.append("agentux-report.json decision.confidence must be Low, Medium, or High")
    if dashboard.get("go_no_go") not in {"go", "review", "hold"}:
        failures.append("agentux-report.json decision_dashboard.go_no_go is required")
    if coverage.get("confidence") not in {"Low", "Medium", "High"}:
        failures.append("agentux-report.json coverage.confidence must be Low, Medium, or High")
    if "blind_spots" not in coverage:
        failures.append("agentux-report.json coverage.blind_spots is required")
    if not coverage.get("source_requirements"):
        failures.append("agentux-report.json coverage.source_requirements is required")
    if not differentiation.get("claims_to_avoid"):
        failures.append("agentux-report.json differentiation.claims_to_avoid is required")
    if not isinstance(search_log, list) or not search_log:
        failures.append("agentux-report.json search_log must include at least one entry")
    if not isinstance(candidates, list) or not candidates:
        failures.append("agentux-report.json candidates must include at least one entry")


def _check_markdown(
    path: Path,
    required_terms: list[str] | list[list[str]],
    failures: list[str],
) -> None:
    text = path.read_text(encoding="utf-8").lower()
    for required in required_terms:
        alternatives = required if isinstance(required, list) else [required]
        if not any(term in text for term in alternatives):
            failures.append(f"{path.name} must mention {' or '.join(alternatives)}")


def _dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _positive_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.isdecimal():
        return int(value)
    return None


if __name__ == "__main__":
    raise SystemExit(main())
