from __future__ import annotations

import argparse
from datetime import UTC, datetime
from pathlib import Path

from project_scout.core import build_report, load_brief, load_candidates, load_url_candidates
from project_scout.github import search_github_repositories
from project_scout.models import CandidateRepo
from project_scout.report import write_report
from project_scout.skills_registry import search_skills_registry


def main(argv: list[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    if args.command == "report":
        return _report(args)
    parser.print_help()
    return 1


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="project-scout")
    subparsers = parser.add_subparsers(dest="command")
    report = subparsers.add_parser("report", help="Generate a prior-art report.")
    report.add_argument("--brief", required=True, help="Path to project brief JSON.")
    report.add_argument(
        "--candidates",
        action="append",
        default=[],
        help="Path to candidate repository JSON. May be passed more than once.",
    )
    report.add_argument(
        "--urls",
        action="append",
        default=[],
        help="Path to a newline-delimited manual URL list. May be passed more than once.",
    )
    report.add_argument("--github-query", help="Unauthenticated GitHub repository search query.")
    report.add_argument("--github-limit", type=int, default=10, help="Maximum GitHub results.")
    report.add_argument("--skills-query", help="Search installed skills registry via `npx skills find`.")
    report.add_argument("--out-json", default="project-scout-report.json", help="JSON output path.")
    report.add_argument(
        "--out-md",
        default=None,
        help="Markdown output path.",
    )
    report.add_argument("--generated-at", help="Override generated timestamp for repeatable tests.")
    return parser


def _report(args: argparse.Namespace) -> int:
    brief = load_brief(args.brief)
    candidates: list[CandidateRepo] = []
    search_log: list[dict[str, object]] = []
    for candidate_path in args.candidates:
        loaded = load_candidates(candidate_path)
        candidates.extend(loaded)
        search_log.append(
            _search_log_entry("manual", candidate_path, len(loaded), len(loaded), "ok")
        )
    for url_path in args.urls:
        loaded = load_url_candidates(url_path)
        candidates.extend(loaded)
        search_log.append(_search_log_entry("manual", url_path, len(loaded), len(loaded), "ok"))
    if args.github_query:
        loaded = search_github_repositories(args.github_query, limit=max(1, args.github_limit))
        candidates.extend(loaded)
        search_log.append(
            _search_log_entry("github", args.github_query, len(loaded), len(loaded), "ok")
        )
    if args.skills_query:
        try:
            loaded = search_skills_registry(args.skills_query)
        except RuntimeError as exc:
            search_log.append(
                _search_log_entry("skills", args.skills_query, 0, 0, "failed", str(exc))
            )
        else:
            candidates.extend(loaded)
            search_log.append(
                _search_log_entry("skills", args.skills_query, len(loaded), len(loaded), "ok")
            )
    if not candidates:
        raise SystemExit(
            "No candidates provided. Use --candidates, --urls, --github-query, or --skills-query."
        )

    report = build_report(brief, candidates, generated_at=args.generated_at, search_log=search_log)
    out_md = Path(args.out_md or _default_markdown_path())
    write_report(report, out_json=Path(args.out_json), out_md=out_md)
    print(f"Wrote {args.out_json}")
    print(f"Wrote {out_md}")
    return 0


def _default_markdown_path() -> str:
    month = datetime.now(UTC).strftime("%Y-%m")
    return f"docs/research/{month}-prior-art-map.md"


def _search_log_entry(
    source: str,
    query: str,
    result_count: int,
    used_count: int,
    status: str,
    error: str | None = None,
) -> dict[str, object]:
    return {
        "source": source,
        "query": query,
        "result_count": result_count,
        "used_count": used_count,
        "status": status,
        "error": error,
    }


if __name__ == "__main__":
    raise SystemExit(main())
