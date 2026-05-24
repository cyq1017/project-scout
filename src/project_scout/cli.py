from __future__ import annotations

import argparse
from datetime import UTC, datetime
from pathlib import Path

from project_scout.core import build_report, load_brief, load_candidates, load_url_candidates
from project_scout.github import search_github_repositories
from project_scout.models import CandidateRepo
from project_scout.report import write_report


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
    for candidate_path in args.candidates:
        candidates.extend(load_candidates(candidate_path))
    for url_path in args.urls:
        candidates.extend(load_url_candidates(url_path))
    if args.github_query:
        candidates.extend(
            search_github_repositories(args.github_query, limit=max(1, args.github_limit))
        )
    if not candidates:
        raise SystemExit("No candidates provided. Use --candidates, --urls, or --github-query.")

    report = build_report(brief, candidates, generated_at=args.generated_at)
    out_md = Path(args.out_md or _default_markdown_path())
    write_report(report, out_json=Path(args.out_json), out_md=out_md)
    print(f"Wrote {args.out_json}")
    print(f"Wrote {out_md}")
    return 0


def _default_markdown_path() -> str:
    month = datetime.now(UTC).strftime("%Y-%m")
    return f"docs/research/{month}-prior-art-map.md"


if __name__ == "__main__":
    raise SystemExit(main())
