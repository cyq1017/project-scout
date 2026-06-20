from __future__ import annotations

import re
import subprocess

from project_scout.models import CandidateRepo


def parse_skills_find_output(output: str) -> list[CandidateRepo]:
    lines = [_strip_ansi(line).strip() for line in output.splitlines() if line.strip()]
    candidates: list[CandidateRepo] = []
    for index, line in enumerate(lines):
        if line.startswith(("Install with", "└", "├")):
            continue
        if "@" not in line:
            continue
        name = line.split()[0]
        if not _looks_like_skill_id(name):
            continue
        url = _following_url(lines, index)
        candidates.append(
            CandidateRepo(
                name=name,
                url=url,
                kind="skill",
                stars=_installs(line),
                description=f"Skill registry result for {name}.",
                topics=["skill", "skills-registry"],
                language="Markdown",
                readme_summary=line,
            )
        )
    return candidates


def search_skills_registry(query: str, *, timeout: int = 30) -> list[CandidateRepo]:
    try:
        result = subprocess.run(
            ["npx", "--yes", "skills", "find", query],
            check=False,
            text=True,
            capture_output=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"skills search timed out after {exc.timeout} seconds") from exc
    except FileNotFoundError as exc:
        raise RuntimeError("skills registry command unavailable: npx") from exc
    except OSError as exc:
        raise RuntimeError(f"skills registry command failed to start: {exc}") from exc
    if result.returncode != 0:
        raise RuntimeError((result.stderr or result.stdout).strip() or "skills search failed")
    return parse_skills_find_output(result.stdout)


def _following_url(lines: list[str], index: int) -> str:
    for line in lines[index + 1 : index + 3]:
        match = re.search(r"https?://\S+", line)
        if match:
            return match.group(0)
    return ""


def _looks_like_skill_id(value: str) -> bool:
    return "@" in value and ("/" in value.split("@", 1)[0] or "." in value.split("@", 1)[0])


def _installs(line: str) -> int:
    match = re.search(r"(\d+(?:\.\d+)?)K installs", line, flags=re.IGNORECASE)
    if match:
        return int(float(match.group(1)) * 1000)
    match = re.search(r"(\d+) installs", line, flags=re.IGNORECASE)
    if match:
        return int(match.group(1))
    return 0


def _strip_ansi(value: str) -> str:
    return re.sub(r"\x1b\[[0-9;]*m", "", value)
