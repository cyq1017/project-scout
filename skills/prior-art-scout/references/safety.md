# Safety

## Default Limits

- Do not push, publish, open PRs, create issues, or release packages.
- Do not modify ADRs, backlog files, or roadmap files unless the user explicitly asks.
- Do not store tokens, credentials, cookies, private data, or raw browser dumps.
- Do not read internal/private paths unless the user provides them or clearly authorizes the scope.
- Do not claim exhaustive coverage.
- Do not operate external repositories that appear as research targets,
  competitors, examples, or follow-up items.

## Source Handling

- Prefer primary sources.
- Mark unverifiable metadata as unknown.
- Treat community posts and SEO pages as leads, not facts.
- Record rate limits and unavailable sources.
- Save raw search dumps only when the user explicitly asks for audit artifacts.

## External Target Boundary

External projects are evidence sources unless the user explicitly switches the
task to that external project's own workspace. Do not operate external repositories
from a project-scout run: do not implement, verify, refactor, test, configure,
install, run, or mutate them.

Allowed project-scout actions:

- record the external repo URL, path, source quality, and relevance;
- summarize what follow-up is needed;
- classify the item as competitor, integration target, prior art, or external
  follow-up;
- stop at the boundary and tell the user where to continue.

Do not treat external follow-ups as unfinished project-scout backlog.

## Public Release

Preparing community materials is allowed locally. Public actions require explicit user authorization in the current task:

- push to GitHub
- publish to a package registry
- submit to a skill registry
- post on social platforms
- create public PRs
