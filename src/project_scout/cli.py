from __future__ import annotations

import argparse
import importlib.resources
from datetime import UTC, datetime
from pathlib import Path

from project_scout.core import build_report, load_brief, load_candidates, load_url_candidates
from project_scout.github import search_github_repositories
from project_scout.models import CandidateRepo
from project_scout.report import write_report
from project_scout.skills_registry import search_skills_registry
from project_scout.summaries import apply_summary_overrides, load_summary_overrides
from project_scout.web import load_web_candidates


def main(argv: list[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    if args.command == "report":
        return _report(args)
    if args.command == "init-brief":
        return _init_brief(args)
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
    report.add_argument(
        "--web-candidates",
        action="append",
        default=[],
        help="Path to curated web/product/page candidate JSON. May be passed more than once.",
    )
    report.add_argument(
        "--github-query",
        action="append",
        default=[],
        help="Unauthenticated GitHub repository search query. May be passed more than once.",
    )
    report.add_argument("--github-limit", type=int, default=10, help="Maximum GitHub results.")
    report.add_argument("--skills-query", help="Search installed skills registry via `npx skills find`.")
    report.add_argument(
        "--summary-overrides",
        action="append",
        default=[],
        help="Path to optional summary override JSON produced by an external summarizer.",
    )
    report.add_argument("--out-json", default="project-scout-report.json", help="JSON output path.")
    report.add_argument(
        "--out-md",
        default=None,
        help="Markdown output path.",
    )
    report.add_argument("--generated-at", help="Override generated timestamp for repeatable tests.")
    init_brief = subparsers.add_parser("init-brief", help="Copy a reusable brief template.")
    init_brief.add_argument(
        "--template",
        required=True,
        choices=sorted(_BRIEF_TEMPLATES),
        help="Template to copy.",
    )
    init_brief.add_argument("--out", required=True, help="Output path for the new brief JSON.")
    init_brief.add_argument("--force", action="store_true", help="Overwrite an existing output file.")
    return parser


_BRIEF_TEMPLATES = {
    "skill": "skill-discovery.json",
    "cli": "cli-library.json",
    "plugin": "agent-plugin.json",
}


def _init_brief(args: argparse.Namespace) -> int:
    out_path = Path(args.out)
    if out_path.exists() and not args.force:
        raise SystemExit(f"{out_path} already exists. Use --force to overwrite it.")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(_brief_template_bytes(args.template))
    print(f"Wrote {out_path}")
    return 0


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
    for web_path in args.web_candidates:
        loaded = load_web_candidates(web_path)
        candidates.extend(loaded)
        search_log.append(_search_log_entry("web", web_path, len(loaded), len(loaded), "ok"))
    for github_query in args.github_query:
        loaded = search_github_repositories(github_query, limit=max(1, args.github_limit))
        new_candidates = _new_candidates(candidates, loaded)
        candidates.extend(new_candidates)
        search_log.append(
            _search_log_entry("github", github_query, len(loaded), len(new_candidates), "ok")
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
    for summary_path in args.summary_overrides:
        overrides = load_summary_overrides(summary_path)
        candidates, applied = apply_summary_overrides(candidates, overrides)
        search_log.append(
            _search_log_entry(
                "summary_overrides", summary_path, len(overrides), applied, "ok"
            )
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


def _new_candidates(
    candidates: list[CandidateRepo], loaded: list[CandidateRepo]
) -> list[CandidateRepo]:
    seen_urls = {candidate.url for candidate in candidates}
    new_candidates = []
    for candidate in loaded:
        if candidate.url in seen_urls:
            continue
        new_candidates.append(candidate)
        seen_urls.add(candidate.url)
    return new_candidates


def _brief_template_bytes(template: str) -> bytes:
    template_file = _BRIEF_TEMPLATES[template]
    package_path = importlib.resources.files("project_scout").joinpath(
        "brief_templates", template_file
    )
    if package_path.is_file():
        return package_path.read_bytes()

    source_path = (
        Path(__file__).resolve().parents[2] / "examples" / "brief-templates" / template_file
    )
    if source_path.exists():
        return source_path.read_bytes()
    raise SystemExit(f"Missing brief template: {template_file}")


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
